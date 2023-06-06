import elephantbet as ele


ele.open_website()
ele.close_popup()


while True:
    ele.login()
    ele.enter_aviator()
    ele.switch_to_aviator_frame()

    roll_data = ele.RollData()
    roll_data.get()

    ele.logout()




