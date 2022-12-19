# data = [
#     DecisionData(EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y),
#     DecisionData(EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.HIGH, ERun.N),
#     DecisionData(EDayCycle.NIGHT, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y),
#     DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.Y),
#     DecisionData(EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.Y),
#     DecisionData(EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N),
#     DecisionData(EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N),
#     DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.N),
#     DecisionData(EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.N),
#     DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.NORMAL, Soil.LOW, ERun.N),
#     DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.NORMAL, Soil.HIGH, ERun.N),
#     DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N),
#     DecisionData(EDayCycle.NIGHT, Temperature.HOT, Humidity.NORMAL, Soil.LOW, ERun.Y),
#     DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N),
# ]
# day = Stream(data).filter(lambda d: d.dayc == EDayCycle.DAY).to_list()
# day_n_run_n = Stream(day).filter(lambda d: d.run == ERun.N).to_list()
# day_n_run_y = Stream(day).filter(lambda d: d.run == ERun.Y).to_list()
# entropy_day = self.calc_entropy_from_map(len(day), {
#     ERun.N: day_n_run_n,
#     ERun.Y: day_n_run_y
# })
#
# night = Stream(data).filter(lambda d: d.dayc == EDayCycle.NIGHT).to_list()
# night_n_run_n = Stream(night).filter(lambda d: d.run == ERun.N).to_list()
# night_n_run_y = Stream(night).filter(lambda d: d.run == ERun.Y).to_list()
# entropy_night = self.calc_entropy_from_map(len(day), {
#     ERun.N: night_n_run_n,
#     ERun.Y: night_n_run_y
# })
# H_x_S = (len(day) * entropy_day + len(night) * entropy_night) / len(data)
