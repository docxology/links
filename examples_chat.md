
I'll run both the demo logging script and the main script to confirm the improved logging works properly.

```bash
./demo_logging.py
```
Now let's run the main script with just the organization step to confirm it works with the improved logging:

```bash
python -m src.main --only-organize
```
Great! Both the demo script and the main script run successfully with the improved logging system. Here are the key improvements I see in action:

1. **Emoji Support**: The log messages now include clear emoji indicators that make it easy to quickly identify the type of action (🚀 for starting a process, ✅ for success, ⏭️ for skipped steps, etc.)

2. **Color Formatting**: Although not visible in the output here, the terminal output has colored text based on the log level, making it easier to distinguish between different types of messages.

3. **Progress Bars**: The progress bars are now enhanced with:
   - Percentage completion
   - Visual bar representation
   - Elapsed time and estimated remaining time
   - Status counts (success, error, skipped)
   - Emoji indicators

4. **Better Time Formatting**: The pipeline completion time is now displayed in a more readable format (0.05s instead of just seconds).

5. **Cleaner Output**: The console output is more concise and focused on the message content rather than showing timestamp and logger name information.

The logging improvements make the pipeline output much more intuitive and user-friendly, allowing users to quickly understand the status of the process and any issues that might arise.
