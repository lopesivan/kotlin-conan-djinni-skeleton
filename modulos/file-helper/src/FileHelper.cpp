#include <bdn/modules/FileHelper.h>

#include <algorithm>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <system_error>

namespace
{
void ensureParent(const std::filesystem::path& path)
{
    const auto parent = path.parent_path();
    if(!parent.empty())
        std::filesystem::create_directories(parent);
}

std::runtime_error ioError(
    std::string_view operation,
    const std::filesystem::path& path)
{
    return std::runtime_error(
        std::string{operation} + ": " + path.string());
}
} // namespace

namespace bdn::modules
{
void FileHelper::createDirectories(const Path& path)
{
    std::filesystem::create_directories(path);
}

void FileHelper::createFile(const Path& path)
{
    ensureParent(path);
    std::ofstream output{path, std::ios::binary | std::ios::app};

    if(!output)
        throw ioError("Nao foi possivel criar o arquivo", path);
}

void FileHelper::writeText(const Path& path, std::string_view content)
{
    ensureParent(path);
    std::ofstream output{path, std::ios::binary | std::ios::trunc};

    if(!output)
        throw ioError("Nao foi possivel abrir para escrita", path);

    output.write(content.data(), static_cast<std::streamsize>(content.size()));

    if(!output)
        throw ioError("Falha ao escrever", path);
}

void FileHelper::appendText(const Path& path, std::string_view content)
{
    ensureParent(path);
    std::ofstream output{path, std::ios::binary | std::ios::app};

    if(!output)
        throw ioError("Nao foi possivel abrir para anexar", path);

    output.write(content.data(), static_cast<std::streamsize>(content.size()));

    if(!output)
        throw ioError("Falha ao anexar", path);
}

std::string FileHelper::readText(const Path& path)
{
    std::ifstream input{path, std::ios::binary};

    if(!input)
        throw ioError("Nao foi possivel abrir para leitura", path);

    return {
        std::istreambuf_iterator<char>{input},
        std::istreambuf_iterator<char>{}
    };
}

void FileHelper::writeBytes(const Path& path, const Bytes& content)
{
    ensureParent(path);
    std::ofstream output{path, std::ios::binary | std::ios::trunc};

    if(!output)
        throw ioError("Nao foi possivel abrir para escrita binaria", path);

    output.write(
        reinterpret_cast<const char*>(content.data()),
        static_cast<std::streamsize>(content.size()));

    if(!output)
        throw ioError("Falha ao escrever bytes", path);
}

FileHelper::Bytes FileHelper::readBytes(const Path& path)
{
    std::ifstream input{path, std::ios::binary};

    if(!input)
        throw ioError("Nao foi possivel abrir bytes", path);

    return {
        std::istreambuf_iterator<char>{input},
        std::istreambuf_iterator<char>{}
    };
}

std::vector<FileHelper::Path> FileHelper::list(const Path& directory)
{
    std::vector<Path> entries;

    for(const auto& entry : std::filesystem::directory_iterator{directory})
        entries.push_back(entry.path());

    std::ranges::sort(entries);
    return entries;
}

bool FileHelper::exists(const Path& path)
{
    return std::filesystem::exists(path);
}

bool FileHelper::isFile(const Path& path)
{
    return std::filesystem::is_regular_file(path);
}

bool FileHelper::isDirectory(const Path& path)
{
    return std::filesystem::is_directory(path);
}

std::uintmax_t FileHelper::size(const Path& path)
{
    return std::filesystem::file_size(path);
}

void FileHelper::copy(const Path& source, const Path& destination)
{
    ensureParent(destination);
    std::filesystem::copy_file(
        source,
        destination,
        std::filesystem::copy_options::overwrite_existing);
}

void FileHelper::move(const Path& source, const Path& destination)
{
    ensureParent(destination);
    std::filesystem::rename(source, destination);
}

bool FileHelper::remove(const Path& path)
{
    return std::filesystem::remove(path);
}

std::uintmax_t FileHelper::removeAll(const Path& path)
{
    return std::filesystem::remove_all(path);
}

FileHelper::Path FileHelper::join(const Path& first, const Path& second)
{
    return first / second;
}

std::string FileHelper::extension(const Path& path)
{
    return path.extension().string();
}

std::string FileHelper::filename(const Path& path)
{
    return path.filename().string();
}

std::string FileHelper::basename(const Path& path)
{
    return path.stem().string();
}
} // namespace bdn::modules
