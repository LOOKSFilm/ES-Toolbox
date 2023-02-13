import dearpygui.dearpygui as dpg
import login


dpg.create_context()

#define gui theme
with dpg.theme() as maintheme:
    with dpg.theme_component(dpg.mvAll):
        #dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0, 1, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255,118,0,232))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255,118,0,232))
        dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (255,118,0,170))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (255,118,0,232))

        #dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 10)

dpg.create_viewport(title='ES Toolbox', height=600, width=800)
dpg.set_viewport_resizable(False)
dpg.setup_dearpygui()
dpg.show_viewport()
login.loginpage(maintheme)
dpg.start_dearpygui()
dpg.destroy_context()