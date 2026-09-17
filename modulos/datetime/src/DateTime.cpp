#include <bdn/modules/DateTime.h>

#include <date/date.h>

#include <sstream>
#include <stdexcept>

namespace
{
template<typename Value>
Value parseValue(std::string_view text, std::string_view pattern)
{
    Value value{};
    std::istringstream input{std::string{text}};
    input >> date::parse(std::string{pattern}, value);

    if(input.fail())
        throw std::invalid_argument(
            "Data ou hora invalida: " + std::string{text});

    input >> std::ws;
    if(!input.eof())
        throw std::invalid_argument(
            "Caracteres extras na data ou hora: " + std::string{text});

    return value;
}
} // namespace

namespace bdn::modules
{
DateTime::TimePoint DateTime::fromString(std::string_view value)
{
    return fromString(value, "%F %T");
}

DateTime::TimePoint DateTime::fromString(
    std::string_view value,
    std::string_view format)
{
    return date::floor<std::chrono::seconds>(
        parseValue<TimePoint>(value, format));
}

std::string DateTime::toString(const TimePoint& value)
{
    return format(value, "%F %T");
}

std::string DateTime::format(
    const TimePoint& value,
    std::string_view pattern)
{
    return date::format(
        std::string{pattern},
        date::floor<std::chrono::seconds>(value));
}

DateTime::TimePoint DateTime::now()
{
    return date::floor<std::chrono::seconds>(
        std::chrono::system_clock::now());
}

std::string DateTime::nowAsString()
{
    return toString(now());
}

DateTime::TimePoint DateTime::fromSeconds(std::int64_t value)
{
    return TimePoint{std::chrono::seconds{value}};
}

DateTime::TimePoint DateTime::fromMilliseconds(std::int64_t value)
{
    return TimePoint{std::chrono::milliseconds{value}};
}

std::int64_t DateTime::toSeconds(const TimePoint& value)
{
    return std::chrono::duration_cast<std::chrono::seconds>(
               value.time_since_epoch())
        .count();
}

std::int64_t DateTime::toMilliseconds(const TimePoint& value)
{
    return std::chrono::duration_cast<std::chrono::milliseconds>(
               value.time_since_epoch())
        .count();
}

std::int64_t DateTime::currentSeconds()
{
    return toSeconds(std::chrono::system_clock::now());
}

std::int64_t DateTime::currentMilliseconds()
{
    return toMilliseconds(std::chrono::system_clock::now());
}

std::int64_t DateTime::millisecondsFromTimeString(std::string_view value)
{
    if(value.empty())
        return 0;

    const auto duration =
        parseValue<std::chrono::milliseconds>(value, "%T");

    return duration.count();
}
} // namespace bdn::modules
