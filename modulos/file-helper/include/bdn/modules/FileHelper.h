#pragma once

#include <cstdint>
#include <filesystem>
#include <string>
#include <string_view>
#include <vector>

namespace bdn::modules
{
class FileHelper final
{
  public:
    using Path = std::filesystem::path;
    using Bytes = std::vector<std::uint8_t>;

    FileHelper() = delete;

    static void createDirectories(const Path& path);
    static void createFile(const Path& path);

    static void writeText(const Path& path, std::string_view content);
    static void appendText(const Path& path, std::string_view content);
    static std::string readText(const Path& path);

    static void writeBytes(const Path& path, const Bytes& content);
    static Bytes readBytes(const Path& path);

    static std::vector<Path> list(const Path& directory);

    static bool exists(const Path& path);
    static bool isFile(const Path& path);
    static bool isDirectory(const Path& path);
    static std::uintmax_t size(const Path& path);

    static void copy(const Path& source, const Path& destination);
    static void move(const Path& source, const Path& destination);
    static bool remove(const Path& path);
    static std::uintmax_t removeAll(const Path& path);

    static Path join(const Path& first, const Path& second);
    static std::string extension(const Path& path);
    static std::string filename(const Path& path);
    static std::string basename(const Path& path);
};
} // namespace bdn::modules
