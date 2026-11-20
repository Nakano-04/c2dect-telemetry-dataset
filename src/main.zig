const std = @import("std");

var global_io: std.Io = undefined;

fn out(allocator: std.mem.Allocator, comptime fmt: []const u8, args: anytype) !void {
    const text = try std.fmt.allocPrint(allocator, fmt, args);
    defer allocator.free(text);
    try std.Io.File.stdout().writeStreamingAll(global_io, text);
}

fn isSecretKey(key: []const u8) bool {
    return contains(key, "password") or contains(key, "token") or
        contains(key, "secret") or contains(key, "api_key");
}

fn contains(haystack: []const u8, needle: []const u8) bool {
    return std.mem.indexOf(u8, haystack, needle) != null;
}

fn pseudonym(allocator: std.mem.Allocator, value: []const u8) ![]u8 {
    var hasher = std.crypto.hash.sha2.Sha256.init(.{});
    hasher.update(value);
    var digest: [32]u8 = undefined;
    hasher.final(&digest);
    const hex = std.fmt.bytesToHex(digest, .lower);
    return std.fmt.allocPrint(allocator, "host-{s}", .{hex[0..10]});
}

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    global_io = init.io;
    const args = try init.minimal.args.toSlice(allocator);
    if (args.len < 2) {
        try out(allocator, "uso: dataset_zig <telemetry.jsonl>\n", .{});
        std.process.exit(2);
    }

    const data = try std.Io.Dir.cwd().readFileAlloc(global_io, args[1], allocator, std.Io.Limit.limited(16 * 1024 * 1024));
    defer allocator.free(data);

    var by_tech = std.StringHashMap(usize).init(allocator);
    defer {
        var it = by_tech.keyIterator();
        while (it.next()) |key| allocator.free(key.*);
        by_tech.deinit();
    }
    var events: usize = 0;

    var lines = std.mem.splitScalar(u8, data, '\n');
    while (lines.next()) |raw| {
        const line = std.mem.trim(u8, raw, " \t\r");
        if (line.len == 0) continue;

        const parsed = try std.json.parseFromSlice(std.json.Value, allocator, line, .{});
        defer parsed.deinit();
        var obj = parsed.value.object;

        var to_remove = std.ArrayList([]const u8).empty;
        defer to_remove.deinit(allocator);
        var it = obj.iterator();
        while (it.next()) |entry| {
            if (isSecretKey(entry.key_ptr.*)) {
                try to_remove.append(allocator, entry.key_ptr.*);
            }
        }
        for (to_remove.items) |key| _ = obj.orderedRemove(key);

        if (obj.getPtr("host")) |host| {
            if (host.* == .string) {
                host.* = .{ .string = try pseudonym(allocator, host.string) };
            }
        }

        if (obj.get("technique")) |tech| {
            const key = try allocator.dupe(u8, tech.string);
            const entry = try by_tech.getOrPut(key);
            if (!entry.found_existing) entry.value_ptr.* = 0;
            entry.value_ptr.* += 1;
        }
        events += 1;
    }

    try out(allocator, "{{\"events\":{d},\"techniques\":{d}}}\n", .{ events, by_tech.count() });
    var it = by_tech.iterator();
    while (it.next()) |entry| {
        try out(allocator, "  {s}: {d}\n", .{ entry.key_ptr.*, entry.value_ptr.* });
    }
}

test "isSecretKey" {
    try std.testing.expect(isSecretKey("password"));
    try std.testing.expect(isSecretKey("api_key"));
    try std.testing.expect(!isSecretKey("technique"));
}
