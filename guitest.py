import easygui

try:
    guy = easygui.buttonbox(msg="testingthing", title="titlething", cancel_choice="cancel", default_choice="bruh").choice
    print(guy)
except:
    print("you cancelled")
    raise SystemExit