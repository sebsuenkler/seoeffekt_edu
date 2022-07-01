def write_to_log(timestamp, content):
    f = open("tool.log", "a+")
    f.write(timestamp+": "+content+"\n")
    f.close()
