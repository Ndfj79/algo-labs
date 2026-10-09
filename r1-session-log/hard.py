import sys
import time


if len(sys.argv) < 3:
    print("Введите название файлов")
else:
    log_file = sys.argv[1]
    res_file = sys.argv[2]
    sessions = {}
    logins = {}
    string_count = 0
    session_count = 0
    peak = [0, 0]
    time_sum = 0
    times = {}
    print(log_file, res_file, file=sys.stderr)

    try:
        with open(log_file, 'r', encoding='utf-8', errors='replace') as file:
            logs = [i for i in file.readlines()]
    except:
        print("Ошибка при открытии файлов")


    with open(res_file, 'w', encoding='utf-8') as file:
        start_time = time.perf_counter()
        for log in logs:
            log = log.split()
            string_count += 1

            if len(log) == 0:
                continue

            if len(log) != 3:
                file.write(f"ERROR {string_count} bad_event\n")
                continue

            if log[0] == "LOGIN":
                sessions[log[1]] = 1
                times[log[1]] = log[2]
                logins[log[1]] = string_count
                if peak[0] < sum(sessions.values()):
                    peak[0] = sum(sessions.values())
                    peak[1] = string_count

            elif log[0] == "LOGOUT":
                if log[1] in sessions.keys():
                    if sessions[log[1]] == 1:
                        sessions[log[1]] = 0
                        session_count += 1
                        time_sum += int(log[2]) - int(times[log[1]])
                    else:
                        file.write(f"ERROR {string_count} logout_without_login\n")
                else:
                    file.write(f"ERROR {string_count} logout_without_login\n")
            else:
                file.write(f"ERROR {string_count} bad_event\n")

        if len(sessions) != 0:
            for i in sessions.keys():
                if sessions[i] == 1:
                    file.write(f"ERROR {logins[i]} session_not_closed\n")
        file.write(f"SESSIONS {session_count}\n")

        print(f"# stats: peak_concurrent={peak[0]} at line={peak[1]}", file=sys.stderr)
        if session_count != 0:
            avg_duration = time_sum / session_count
            print(f"# stats: avg_duration={avg_duration}", file=sys.stderr)

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            print(exec_time, file=sys.stderr)
