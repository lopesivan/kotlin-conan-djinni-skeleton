#pragma once

#include <memory>
#include <mutex>
#include <string>
#include <string_view>

namespace bdn::modules
{
enum class LogLevel
{
    Verbose = 0,
    Debug,
    Info,
    Warning,
    Error
};

class LogSink
{
  public:
    virtual ~LogSink() = default;
    virtual void write(LogLevel level, std::string_view formattedMessage) = 0;
};

class Logger final
{
  public:
    static Logger& shared();

    void setSink(std::shared_ptr<LogSink> sink);
    void setLevel(LogLevel level);
    void setGroup(std::string group);

    [[nodiscard]] LogLevel level() const;
    [[nodiscard]] std::string group() const;
    [[nodiscard]] bool allows(LogLevel level) const;

    void log(LogLevel level, std::string_view message);
    void verbose(std::string_view message);
    void debug(std::string_view message);
    void info(std::string_view message);
    void warning(std::string_view message);
    void error(std::string_view message);

    static std::string_view levelName(LogLevel level);

  private:
    Logger();

    mutable std::mutex mutex_;
    std::shared_ptr<LogSink> sink_;
    LogLevel level_{LogLevel::Debug};
    std::string group_{"Boden"};
};

class StreamLogSink final : public LogSink
{
  public:
    void write(LogLevel level, std::string_view formattedMessage) override;
};
} // namespace bdn::modules
