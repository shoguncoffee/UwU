import datetime
import math

time_1 = datetime.time(20, 10)
time_2 = datetime.time(5, 15)

enter_delta = datetime.timedelta(hours = time_1.hour, minutes = time_1.minute)
exit_delta = datetime.timedelta(hours = time_2.hour, minutes = time_2.minute)
time_diff_delta = enter_delta - exit_delta
print(time_diff_delta)

total_second = time_diff_delta.seconds
print(total_second)
#convert seconds to minutes
total_minute = math.floor(total_second / 60)
print(total_minute)

total_hour = math.floor(math.floor(time_diff_delta.seconds / 60) / 60)
print(total_hour)

remaining_minute = total_minute - (math.floor(math.floor(time_diff_delta.seconds / 60) / 60) * 60)
print(remaining_minute)