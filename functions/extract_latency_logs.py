import re


def extract_latency_logs(source_log_file, output_log_file):
    """
    Extracts latencies from a log file and writes them to a new file.
    """
    latency_pattern = re.compile(r'latency: (\d+\.\d+) seconds')
    setup_pattern = re.compile(
        r'Script last modified|Setup:|chosen_timeout|random_timeout|'
        r'timeout_booking_page|auto_captcha|time_restriction_hour|updater')
    user_pattern = re.compile(r'selected timeslot|OS:|Animations:')
    error_pattern = re.compile(r'ERROR -')
    executed_successfully_pattern = re.compile(r'EXECUTED SUCCESSFULLY: 提交订单')
    session_start_pattern = re.compile(r"New session started at")

    last_executed_successfully = None
    session_successful = False
    first_session = True

    with open(source_log_file, 'r') as source:
        lines_to_write = []

        for line in source:
            if session_start_pattern.search(line):
                if not first_session:
                    success_status = "Successfully submitted!" if session_successful else "Submission failed!"
                    lines_to_write.append(f"Session Status: {success_status}\n")
                    lines_to_write.append('=' * 30 + '\n')
                session_start_time = line.split()[-1]
                lines_to_write.append('=' * 30 + '\n')
                lines_to_write.append(f"Session started at {session_start_time}\n")
                first_session = False
                session_successful = False
            elif setup_pattern.search(line) or user_pattern.search(line) or "seconds" in line:
                lines_to_write.append(line)
            elif latency_pattern.search(line):
                match = latency_pattern.search(line)
                if match:
                    latency = match.group(1)
                    lines_to_write.append(f"{line.strip()} - Extracted Latency: {latency} seconds\n")
            elif executed_successfully_pattern.search(line):
                session_successful = True
                lines_to_write.append(line)
            elif error_pattern.search(line):
                if last_executed_successfully:
                    lines_to_write.append(last_executed_successfully)
                lines_to_write.append(line)
                last_executed_successfully = None

        if not first_session:
            success_status = "Successfully submitted!" if session_successful else "Submission failed!"
            lines_to_write.append(f"Session Status: {success_status}\n")
            lines_to_write.append('=' * 30 + '\n')

        with open(output_log_file, 'w') as output:
            for line in lines_to_write:
                output.write(line)


# Call this function with the path to your main log file and the desired output file for latencies
extract_latency_logs('../booking_logs/SJTU_booking_log.log', 'booking_logs/Stats.log')
