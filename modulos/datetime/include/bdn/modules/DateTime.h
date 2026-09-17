#pragma once

#include <chrono>
#include <cstdint>
#include <string>
#include <string_view>

namespace bdn::modules
{
class DateTime final
{
  public:
    using TimePoint = std::chrono::system_clock::time_point;

    DateTime() = delete;

    static TimePoint fromString(std::string_view value);
    static TimePoint fromString(std::string_view value, std::string_view format);

    static std::string toString(const TimePoint& value);
    static std::string format(const TimePoint& value, std::string_view pattern);

    static TimePoint now();
    static std::string nowAsString();

    static TimePoint fromSeconds(std::int64_t value);
    static TimePoint fromMilliseconds(std::int64_t value);

    static std::int64_t toSeconds(const TimePoint& value);
    static std::int64_t toMilliseconds(const TimePoint& value);

    static std::int64_t currentSeconds();
    static std::int64_t currentMilliseconds();

    static std::int64_t millisecondsFromTimeString(std::string_view value);
};
} // namespace bdn::modules
