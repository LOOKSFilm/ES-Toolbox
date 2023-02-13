from EditShareAPI import EsAuth
import dearpygui.dearpygui as dpg
import placeholder_transfer

def login():
    global user
    user = dpg.get_value("user")
    pw = dpg.get_value('password')
    server = str(dpg.get_value('server'))
    connect = EsAuth.login(server, user, pw)
    if connect == 200:
        dpg.delete_item('loginwindow')
        placeholder_transfer.main()
    else:
        if dpg.does_item_exist('wrong') == True:
            dpg.delete_item('wrong')
            dpg.add_text(default_value='Wrong pw or username!', parent='bot', tag='wrong')
        else:
            dpg.add_text(default_value='Wrong pw or username!', parent='bot', tag='wrong')

def loginpage(maintheme):
    with dpg.window(tag='loginwindow') as loginwindow:
        dpg.bind_item_theme(loginwindow, maintheme)
        dpg.set_primary_window('loginwindow', True)
        with dpg.table(tag='logintable', header_row=False):
            dpg.add_table_column(tag="c1",width_stretch=True)
            dpg.add_table_column(tag="c2",width_stretch=True)
            dpg.add_table_column(tag="c3",width_stretch=True)
            with dpg.table_row():
                dpg.add_spacer(height=100)
            with dpg.table_row():
                dpg.add_spacer()
                dpg.add_input_text(label='User', tag="user", on_enter=True, callback=login)
            with dpg.table_row():
                dpg.add_spacer(height=20)
            with dpg.table_row():
                dpg.add_spacer()
                dpg.add_input_text(label='Password', password=True, tag="password", on_enter=True, callback=login)
            with dpg.table_row():
                dpg.add_spacer(height=50)
            with dpg.table_row():
                dpg.add_spacer()
                dpg.add_combo(label='Server', items=["10.0.77.14", "192.168.0.220"], default_value='10.0.77.14', tag="server")
            with dpg.table_row():
                dpg.add_spacer(height=20)
            with dpg.table_row():
                dpg.add_spacer()
                dpg.add_button(label='Login', width=100, callback=login, tag='loginbtn')
            with dpg.table_row(tag='bot'):
                dpg.add_spacer(height=100)