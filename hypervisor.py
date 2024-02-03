# coding=utf-8

import telebot
import base64
import shell
import config
# from shell import shell as shell1

# shell1 = shell.shell
bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=['spawn'], func=lambda message: message.chat.type == "private")
def send_spawn_command_result(message):
    if message.from_user.id == 673748261:
        # bot.send_message(message.chat.id, "in")
        try:
            pwfile = open(config.password_file, "r")
            pwfile_content = pwfile.read().strip()
            # bot.send_message(message.chat.id, pw)
            if pwfile_content is None or pwfile_content != "":
                # bot.send_message(message.chat.id, "aagad")
                pw = base64.urlsafe_b64decode(pwfile_content.encode('utf-8')).decode('utf-8')
                # bot.send_message(message.chat.id, message.text)
                # bot.send_message(message.chat.id, shell.execute_sudo((message.text), pw), parse_mode="Markdown")
                # command_to_run = "tmux new-session -d -s batman " + f"'{shell.split_command(message.text)}" + "; tmux wait-for -S done \; wait-for done \; capture-pane -p -t batman"
                command_to_run = "/usr/bin/tmux new-session -d -s batman " + f"'{shell.split_command(message.text)}" + " ; /usr/bin/tmux wait-for -S done '\; wait-for done \; capture-pane -p -t batman"
                # bot.send_message(message.chat.id, command_to_run)
                bot.send_message(message.chat.id, "```\n" + shell.execute_sudo(command_to_run, pw) + "\n```", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(message.chat.id, e)
    else:
        bot.send_message(message.chat.id, "Error: Permission denied.")






@bot.message_handler(commands=['run'], func=lambda message: message.chat.type == "private")
def send_command_result(message):
    if message.from_user.id in config.admins:
        bot.send_message(message.chat.id, "```\n" + shell.execute_one_line(shell.split_command(message.text)) + "\n```",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Error: Permission denied.")


@bot.message_handler(commands=['su'], func=lambda message: message.chat.type == "private")
def send_su_command_result(message):
    if message.from_user.id == 673748261:
        # bot.send_message(message.chat.id, "in")
        try:
            pwfile = open(config.password_file, "r")
            pwfile_content = pwfile.read().strip()
            # bot.send_message(message.chat.id, pw)
            if pwfile_content is None or pwfile_content != "":
                # bot.send_message(message.chat.id, "aagad")
                pw = base64.urlsafe_b64decode(pwfile_content.encode('utf-8')).decode('utf-8')
                # bot.send_message(message.chat.id, message.text)
                # bot.send_message(message.chat.id, shell.execute_sudo((message.text), pw), parse_mode="Markdown")
                bot.send_message(message.chat.id, "```\n" + shell.execute_sudo(
                    shell.split_command(message.text), pw) + "\n```", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(message.chat.id, e)
    else:
        bot.send_message(message.chat.id, "Error: Permission denied.")


@bot.message_handler(commands=['set_pw'], func=lambda message: message.chat.type == "private")
def set_password(message):
    if message.from_user.id in config.admins:
        pwfile = open(config.password_file, "w")
        password = message.text.split(' ')[1]
        pwfile.write(base64.urlsafe_b64encode(password.encode('utf-8')).decode('utf-8'))
        pwfile.close()
        bot.send_message(message.chat.id, "Done.")
    else:
        bot.send_message(message.chat.id, "Error: Operation not permitted.")

bot.polling()
