#include <bdn/modules/DateTime.h>
#include <bdn/modules/Logger.h>

#include <iostream>
#include <sstream>
#include <utility>

namespace bdn::modules
{
Logger& Logger::shared()
{
    static Logger instance;
    return instance;
}

Logger::Logger()
    : sink_{std::make_shared<StreamLogSink>()}
{
}

void Logger::setSink(std::shared_ptr<LogSink> sink)
{
    std::scoped_lock lock{mutex_};
    sink_ = std::move(sink);
}

void Logger::setLevel(LogLevel level)
{
    std::scoped_lock lock{mutex_};
    level_ = level;
}

void Logger::setGroup(std::string group)
{
    std::scoped_lock lock{mutex_};
    group_ = std::move(group);
}

LogLevel Logger::level() const
{
    std::scoped_lock lock{mutex_};
    return level_;
}

std::string Logger::group() const
{
    std::scoped_lock lock{mutex_};
    return group_;
}

bool Logger::allows(LogLevel level) const
{
    std::scoped_lock lock{mutex_};
    return static_cast<int>(level) >= static_cast<int>(level_);
}

void Logger::log(LogLevel level, std::string_view message)
{
    std::shared_ptr<LogSink> sink;
    std::string group;

    {
        std::scoped_lock lock{mutex_};

        if(static_cast<int>(level) < static_cast<int>(level_))
            return;

        sink = sink_;
        group = group_;
    }

    if(!sink)
        return;

    std::ostringstream formatted;
    formatted << '[' << DateTime::nowAsString() << "] ["
              << levelName(level) << "] [" << group << "] " << message;

    sink->write(level, formatted.str());
}

void Logger::verbose(std::string_view message)
{
    log(LogLevel::Verbose, message);
}

void Logger::debug(std::string_view message)
{
    log(LogLevel::Debug, message);
}

void Logger::info(std::string_view message)
{
    log(LogLevel::Info, message);
}

void Logger::warning(std::string_view message)
{
    log(LogLevel::Warning, message);
}

void Logger::error(std::string_view message)
{
    log(LogLevel::Error, message);
}

std::string_view Logger::levelName(LogLevel level)
{
    switch(level)
    {
        case LogLevel::Verbose:
            return "VERBOSE";
        case LogLevel::Debug:
            return "DEBUG";
        case LogLevel::Info:
            return "INFO";
        case LogLevel::Warning:
            return "WARNING";
        case LogLevel::Error:
            return "ERROR";
    }

    return "UNKNOWN";
}

void StreamLogSink::write(LogLevel level, std::string_view formattedMessage)
{
    auto& stream =
        level >= LogLevel::Warning ? std::cerr : std::clog;
    stream << formattedMessage << '\n';
}
} // namespace bdn::modules
