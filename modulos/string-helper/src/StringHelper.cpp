#include <bdn/modules/StringHelper.h>

#include <algorithm>
#include <cctype>
#include <iomanip>
#include <sstream>

namespace
{
bool isSpace(char value)
{
    return std::isspace(static_cast<unsigned char>(value)) != 0;
}

int hexValue(char value)
{
    if(value >= '0' && value <= '9')
        return value - '0';
    if(value >= 'a' && value <= 'f')
        return value - 'a' + 10;
    if(value >= 'A' && value <= 'F')
        return value - 'A' + 10;
    return -1;
}

bool isUriComponentSafe(unsigned char value)
{
    return std::isalnum(value) != 0 || value == '-' || value == '_' ||
           value == '.' || value == '!' || value == '~' || value == '*' ||
           value == '\'' || value == '(' || value == ')';
}
} // namespace

namespace bdn::modules
{
std::string StringHelper::leftTrim(std::string_view text)
{
    const auto first = std::find_if_not(text.begin(), text.end(), isSpace);
    return {first, text.end()};
}

std::string StringHelper::rightTrim(std::string_view text)
{
    const auto last = std::find_if_not(text.rbegin(), text.rend(), isSpace).base();
    return {text.begin(), last};
}

std::string StringHelper::trim(std::string_view text)
{
    const auto first = std::find_if_not(text.begin(), text.end(), isSpace);
    const auto last = std::find_if_not(text.rbegin(), text.rend(), isSpace).base();

    if(first >= last)
        return {};

    return {first, last};
}

std::string StringHelper::toLower(std::string_view text)
{
    std::string result{text};
    std::ranges::transform(result, result.begin(), [](unsigned char value) {
        return static_cast<char>(std::tolower(value));
    });
    return result;
}

std::string StringHelper::toUpper(std::string_view text)
{
    std::string result{text};
    std::ranges::transform(result, result.begin(), [](unsigned char value) {
        return static_cast<char>(std::toupper(value));
    });
    return result;
}

std::vector<std::string> StringHelper::split(
    std::string_view text,
    std::string_view separators,
    bool trimEmpty)
{
    std::vector<std::string> result;

    if(separators.empty())
    {
        if(!text.empty() || !trimEmpty)
            result.emplace_back(text);
        return result;
    }

    std::size_t begin = 0;
    while(begin <= text.size())
    {
        const auto end = text.find_first_of(separators, begin);
        const auto token = text.substr(
            begin,
            end == std::string_view::npos ? text.size() - begin : end - begin);

        if(!token.empty() || !trimEmpty)
            result.emplace_back(token);

        if(end == std::string_view::npos)
            break;

        begin = end + 1;
    }

    return result;
}

std::string StringHelper::encodeUri(std::string_view text)
{
    std::ostringstream result;
    result << std::uppercase << std::hex;

    for(const unsigned char value : text)
    {
        if(isUriComponentSafe(value))
            result << static_cast<char>(value);
        else
            result << '%' << std::setw(2) << std::setfill('0')
                   << static_cast<unsigned int>(value);
    }

    return result.str();
}

std::string StringHelper::decodeUri(std::string_view text)
{
    std::string result;
    result.reserve(text.size());

    for(std::size_t index = 0; index < text.size(); ++index)
    {
        if(text[index] == '%' && index + 2 < text.size())
        {
            const int high = hexValue(text[index + 1]);
            const int low = hexValue(text[index + 2]);

            if(high >= 0 && low >= 0)
            {
                result.push_back(static_cast<char>((high << 4) | low));
                index += 2;
                continue;
            }
        }

        result.push_back(text[index]);
    }

    return result;
}
} // namespace bdn::modules
