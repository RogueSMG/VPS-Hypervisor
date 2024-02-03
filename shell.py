import os
import subprocess
import config


def execute_one_line(command):
    if command is not None:
        #if int(os.getegid()) == 0 and config.normal_user != "":
            # print(config.normal_user)
            # command = "su -c " + command
            # print("hi")
        if "exit" in command:
            return "Error: Unfortunately I do not accept exit"
        command += "; exit 0"
        result = subprocess.check_output(command, shell=True).decode('utf-8')
        # print(command)
        real_result = ''
        if "[sudo] password for" in result:
            results = result.split(': ')
            if len(results) > 1:
                for arg in results:
                    if results.index(arg) > 0:
                        real_result += arg + ""
        # print(real_result)
        else:
            real_result = result
        # print(real_result)
        return real_result.strip()
    else:
        return "Error: Command is null"


def execute_sudo(command, passwd):
    if command is not None:
        # print(config.normal_user)
        # print(command)
        # print(execute_one_line("echo '" + passwd + "' | sudo -c "  + command))
        return execute_one_line("echo '" + passwd + "' | sudo "  + command)
    else:
        return "Error: Command is null"


def split_command(message):
    commands = message.split(' ')
    args = ""
    for arg in commands:
        if commands.index(arg) > 0:
            args += arg + " "
    # print(args.strip())
    return args.strip()
