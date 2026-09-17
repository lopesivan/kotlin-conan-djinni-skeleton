#pragma once

#include <string>
#include <string_view>
#include <vector>

namespace bdn::modules
{
class StringHelper final
{
  public:
    StringHelper() = delete;

    static std::string trim(std::string_view text);
    static std::string leftTrim(std::string_view text);
    static std::string rightTrim(std::string_view text);
    static std::string toLower(std::string_view text);
    static std::string toUpper(std::string_view text);

    // separators is treated as a set of delimiter characters.
    static std::vector<std::string> split(
        std::string_view text,
        std::string_view separators,
        bool trimEmpty = true);

    static std::string encodeUri(std::string_view text);
    static std::string decodeUri(std::string_view text);
};
} // namespace bdn::modules
