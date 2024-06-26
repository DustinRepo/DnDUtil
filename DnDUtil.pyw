from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import sys
import math
import array

# Global variables
hit_positions: array = ["Head", "Body", "Arms", "Legs", "Hands/Feet"]

phys_damage_weapon_damage: int = 0
phys_damage_phys_power: float = 0
phys_damage_added_damage: float = 0
phys_damage_hit_part_selection: int = 1
phys_damage_target_pdr: float = 0
phys_damage_armor_pen: float = 0
phys_damage_true_phys_damage: int = 0
phys_damage_combo_multiplier: float = 1

magic_damage_skill_spell_damage: int = 0
magic_damage_magic_power: float = 0
magic_damage_magic_weapon_damage: int = 0
magic_damage_added_magic_damage: float = 0
magic_damage_target_mdr: float = 0
magic_damage_magic_pen: float = 0
magic_damage_true_magic_damage: int = 0
magic_damage_attribute_scale: float = 1
magic_damage_hit_part_selection: int = 1

health_strength: int = 0
health_vigor: int = 0
health_max_health_bonus: float = 0
health_added_health: int = 0

action_speed_agility: int = 0
action_speed_dexterity: int = 0
action_speed_action_speed_bonus: float = 0

def main():
    # Create window and ImGui context
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    # Remove INI file
    imgui.get_io().ini_file_name = ""
    imgui.get_io().config_flags |= imgui.CONFIG_NAV_ENABLE_KEYBOARD
    selected: int = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # Tell imgui to start a new frame
        imgui.new_frame()
        # Get variables for creating the buttons
        window_size: tuple = glfw.get_window_size(window)
        button_width: float = window_size[0] / 4 - 10

        # Render stuff for application
        imgui.core.set_next_window_position(0, 0)
        imgui.core.set_next_window_size(window_size[0], window_size[1])
        imgui.begin("DnD Util", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        # Top buttons to select what util to use
        imgui.push_style_color(imgui.COLOR_BUTTON, 1.0, 0.5, 0.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 1.0, 0.7, 0.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7, 0.2, 0.0)
        if imgui.button("Phys Damage", button_width):
            selected = 0
        imgui.pop_style_color(3)
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.5, 0.1, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.7, 0.3, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.0, 0.7)
        if imgui.button("Magic Damage", button_width):
            selected = 1
        imgui.pop_style_color(3)
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.7, 0.1)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.0, 0.9, 0.1)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.0, 0.4, 0.0)
        if imgui.button("Health", button_width):
            selected = 2
        imgui.pop_style_color(3)
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.7, 0.3, 0.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.5, 0.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.4, 0.0, 0.0)
        if imgui.button("Action Speed", button_width):
            selected = 3
        imgui.pop_style_color(3)

        # Show selected window
        if selected == 0:
            phys_damage_window()
        elif selected == 1:
            magic_damage_window()
        elif selected == 2:
            health_window()
        elif selected == 3:
            action_speed_window()

        # Reset imgui and render
        imgui.end()
        gl.glClearColor(0.0, 0.0, 0.0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def hit_part_combo(selected: int):
    global hit_positions
    if imgui.begin_combo("Body Part Hit", hit_positions[selected]):
        for i, item in enumerate(hit_positions):
            is_selected = i == selected
            if imgui.selectable(item, is_selected)[0]:
                selected = i

            if is_selected:
                imgui.set_item_default_focus()
        imgui.end_combo()
    return selected


def gear_rarity_combo(selected: int):
    global gear_rarity
    if imgui.begin_combo("Rarity", gear_rarity[selected]):
        for i, item in enumerate(gear_rarity):
            is_selected = i == selected
            if imgui.selectable(item, is_selected)[0]:
                selected = i

            if is_selected:
                imgui.set_item_default_focus()
        imgui.end_combo()
    return selected


def get_hit_part_multiplier(selected: int):
    if selected == 0:
        return 1.5
    elif selected == 1:
        return 1
    elif selected == 2:
        return 0.8
    elif selected == 3:
        return 0.6
    elif selected == 4:
        return 0.5
    return 1


def phys_damage_window():
    imgui.text("Physical Damage Calculator")
    imgui.new_line()
    imgui.push_item_width(200)
    global phys_damage_weapon_damage
    changed, phys_damage_weapon_damage = imgui.core.input_int("Weapon Damage", phys_damage_weapon_damage)
    global phys_damage_phys_power
    changed, phys_damage_phys_power = imgui.core.input_float("Phys Power Bonus %", phys_damage_phys_power, step=0.1, format="%.1f")
    global phys_damage_added_damage
    changed, phys_damage_added_damage = imgui.core.input_int("Added Physical Damage", phys_damage_added_damage)
    global phys_damage_target_pdr
    changed, phys_damage_target_pdr = imgui.core.input_float("Target PDR %", phys_damage_target_pdr, step=0.1, format="%.1f")
    global phys_damage_armor_pen
    changed, phys_damage_armor_pen = imgui.core.input_float("Armor Pen %", phys_damage_armor_pen, step=0.1, format="%.1f")
    global phys_damage_true_phys_damage
    changed, phys_damage_true_phys_damage = imgui.core.input_int("True Phys Damage", phys_damage_true_phys_damage)
    global phys_damage_combo_multiplier
    changed, phys_damage_combo_multiplier = imgui.core.input_float("Weapon Combo Multiplier", phys_damage_combo_multiplier, step=0.1, format="%.3f")
    global phys_damage_hit_part_selection
    phys_damage_hit_part_selection = hit_part_combo(phys_damage_hit_part_selection)
    imgui.pop_item_width()

    phys_damage_hit_part_multi: float = get_hit_part_multiplier(phys_damage_hit_part_selection)
    phys_damage_phys_power_perc: float = phys_damage_phys_power / 100.0
    phys_damage_target_pdr_perc: float = phys_damage_target_pdr / 100.0
    phys_damage_armor_pen_perc: float = phys_damage_armor_pen / 100.0

    # https://darkanddarker.wiki.spellsandguns.com/Damage_Calculation#Damage_Formula
    phys_damage: float = ( (
        phys_damage_weapon_damage * phys_damage_combo_multiplier
        * (1 + phys_damage_phys_power_perc)
        + phys_damage_added_damage
        )
        * phys_damage_hit_part_multi
        * (1 - phys_damage_target_pdr_perc * (1 - phys_damage_armor_pen_perc))
        + phys_damage_true_phys_damage
    )

    dummy_phys_damage: float = ( (
        phys_damage_weapon_damage * phys_damage_combo_multiplier
        * (1 + phys_damage_phys_power_perc)
        + phys_damage_added_damage
        )
        * phys_damage_hit_part_multi
        # Dummys have -12% pdr ( https://darkanddarker.wiki.spellsandguns.com/Monsters#Dummy )
        * (1 - -0.12 * (1 - phys_damage_armor_pen_perc))
        + phys_damage_true_phys_damage
    )

    imgui.new_line()
    imgui.text("Total Physical Damage: %.2f" % phys_damage)
    imgui.text("Dummy Damage: %d" % math.floor(dummy_phys_damage))


def magic_damage_window():
    imgui.text("Magical Damage Calculator")
    imgui.new_line()
    imgui.push_item_width(200)
    global magic_damage_skill_spell_damage
    changed, magic_damage_skill_spell_damage = imgui.core.input_int("Skill/Spell Damage", magic_damage_skill_spell_damage)
    global magic_damage_magic_power
    changed, magic_damage_magic_power = imgui.core.input_float("Magic Power Bonus %", magic_damage_magic_power, step=0.1, format="%.1f")
    global magic_damage_magic_weapon_damage
    changed, magic_damage_magic_weapon_damage = imgui.core.input_int("Magic Weapon Damage", magic_damage_magic_weapon_damage)
    global magic_damage_added_magic_damage
    changed, magic_damage_added_magic_damage = imgui.core.input_int("Added Magic Damage", magic_damage_added_magic_damage)
    global magic_damage_target_mdr
    changed, magic_damage_target_mdr = imgui.core.input_float("Target MDR %", magic_damage_target_mdr, step=0.1, format="%.1f")
    global magic_damage_magic_pen
    changed, magic_damage_magic_pen = imgui.core.input_float("Magic Penetration", magic_damage_magic_pen, step=0.1, format="%.1f")
    global magic_damage_true_magic_damage
    changed, magic_damage_true_magic_damage = imgui.core.input_int("True Magic Damage", magic_damage_true_magic_damage)
    global magic_damage_attribute_scale
    changed, magic_damage_attribute_scale = imgui.core.input_float("Attribute Scale", magic_damage_attribute_scale, step=0.1, format="%.1f")
    global magic_damage_hit_part_selection
    magic_damage_hit_part_selection = hit_part_combo(magic_damage_hit_part_selection)
    imgui.pop_item_width()

    magic_damage_hit_part_multi: float = get_hit_part_multiplier(magic_damage_hit_part_selection)
    magic_damage_magic_power_perc: float = magic_damage_magic_power / 100.0
    magic_damage_target_mdr_perc: float = magic_damage_target_mdr / 100.0
    magic_damage_magic_pen_perc: float = magic_damage_magic_pen / 100.0

    # https://darkanddarker.wiki.spellsandguns.com/Damage_Calculation#Damage_Formula
    magic_damage: float = ( (
        (magic_damage_skill_spell_damage + (magic_damage_magic_weapon_damage * magic_damage_attribute_scale))
        * (1 + magic_damage_magic_power_perc * magic_damage_attribute_scale)
        + magic_damage_added_magic_damage * magic_damage_attribute_scale
        )
        * magic_damage_hit_part_multi
        * (1 - magic_damage_target_mdr_perc * (1 - magic_damage_magic_pen_perc))
        + (magic_damage_true_magic_damage * magic_damage_attribute_scale)
    )

    dummy_magic_damage: float = ( (
        (magic_damage_skill_spell_damage + (magic_damage_magic_weapon_damage * magic_damage_attribute_scale))
        * (1 + magic_damage_magic_power_perc * magic_damage_attribute_scale)
        + magic_damage_added_magic_damage * magic_damage_attribute_scale
        )
        * magic_damage_hit_part_multi
        # Dummy has 0% MDR so remove MDR calc entirely ( https://darkanddarker.wiki.spellsandguns.com/Monsters#Dummy )
        + (magic_damage_true_magic_damage * magic_damage_attribute_scale)
    )

    imgui.new_line()
    imgui.text("Total Magical Damage: %.2f" % magic_damage)
    imgui.text("Dummy Damage: %d" % math.floor(dummy_magic_damage))


def health_window():
    imgui.text("Health Calculator")
    imgui.new_line()
    imgui.push_item_width(200)
    global health_strength
    changed, health_strength = imgui.core.input_int("Strength", health_strength)
    global health_vigor
    changed, health_vigor = imgui.core.input_int("Vigor", health_vigor)
    global health_max_health_bonus
    changed, health_max_health_bonus = imgui.core.input_float("Max Health Bonus %", health_max_health_bonus, step=0.1, format="%.1f")
    global health_added_health
    changed, health_added_health = imgui.core.input_int("Added Health", health_added_health)
    imgui.pop_item_width()

    health: float = get_total_health(health_strength, health_vigor, health_max_health_bonus / 100.0, health_added_health)
    health_recovery_bonus: int = get_total_health_recovery_bonus(health_vigor)
    health_recovery_rate: float = 1 + (1 * (health_recovery_bonus / 100.0))

    imgui.new_line()
    imgui.text("Total Health: %d" % math.ceil(health))
    imgui.text("Health Recovery Bonus: {}%".format(health_recovery_bonus))
    imgui.text("Resting Health Recovered: %.2f every 2 seconds" % health_recovery_rate)


def action_speed_window():
    imgui.text("Action Speed Calculator")
    imgui.new_line()
    imgui.push_item_width(200)
    global action_speed_agility
    changed, action_speed_agility = imgui.core.input_int("Agility", action_speed_agility)
    global action_speed_dexterity
    changed, action_speed_dexterity = imgui.core.input_int("Dexterity", action_speed_dexterity)
    global action_speed_action_speed_bonus
    changed, action_speed_action_speed_bonus = imgui.core.input_float("Action Speed Bonus %", action_speed_action_speed_bonus, step=0.1, format="%.1f")
    imgui.pop_item_width()

    action_speed: float = get_total_action_speed(action_speed_agility, action_speed_dexterity, action_speed_action_speed_bonus)

    imgui.new_line()
    imgui.text("Total Action Speed: %.2f" % action_speed)


# https://darkanddarker.wiki.spellsandguns.com/Stats#Max_Health
def get_total_health(strength: int, vigor: int, max_health_bonus: float, added_health: int):
    health_sum: float = strength * 0.25 + vigor * 0.75
    base_health: float = 60.0

    while health_sum > 75:
        base_health += 0.5
        health_sum -= 1
    while health_sum > 50:
        base_health += 1.0
        health_sum -= 1
    while health_sum > 10:
        base_health += 2.0
        health_sum -= 1
    if 1 > health_sum > 0:
        base_health += 3.0 * health_sum
    else:
        while health_sum > 0:
            base_health += 3.0
            health_sum -= 1
            if 1 > health_sum > 0:
                base_health += 3.0 * health_sum
                health_sum = 0
    return base_health * (1 + max_health_bonus) + added_health


# https://darkanddarker.wiki.spellsandguns.com/Stats#Health_Recovery
def get_total_health_recovery_bonus(vigor: int):
    health_recovery_bonus: int = -55

    while vigor > 86:
        health_recovery_bonus += 2
        vigor -= 1
    while vigor > 85:
        health_recovery_bonus += 3
        vigor -= 1
    while vigor > 84:
        health_recovery_bonus += 1
        vigor -= 1
    while vigor > 35:
        health_recovery_bonus += 2
        vigor -= 1
    while vigor > 25:
        health_recovery_bonus += 5
        vigor -= 1
    while vigor > 15:
        health_recovery_bonus += 7
        vigor -= 1
    while vigor > 5:
        health_recovery_bonus += 3
        vigor -= 1
    while vigor > 0:
        health_recovery_bonus += 5
        vigor -= 1
    return health_recovery_bonus


# https://darkanddarker.wiki.spellsandguns.com/Stats#Action_Speed
def get_total_action_speed(agility: int, dexterity: int, action_speed_bonus):
    action_speed_sum: float = agility * 0.25 + dexterity * 0.75
    base_action_speed: float = -38.0
    while action_speed_sum > 50:
        base_action_speed += 0.5
        action_speed_sum -= 1
    while action_speed_sum > 41:
        base_action_speed += 1.0
        action_speed_sum -= 1
    while action_speed_sum > 25:
        base_action_speed += 1.5
        action_speed_sum -= 1
    while action_speed_sum > 13:
        base_action_speed += 1.0
        action_speed_sum -= 1
    while action_speed_sum > 10:
        base_action_speed += 2
        action_speed_sum -= 1
    if 1 > action_speed_sum > 0:
        base_action_speed += 3.0 * action_speed_sum
    else:
        while action_speed_sum > 0:
            base_action_speed += 3.0
            action_speed_sum -= 1
            if 1 > action_speed_sum > 0:
                base_action_speed += 3.0 * action_speed_sum
                action_speed_sum = 0
    return base_action_speed + action_speed_bonus


def impl_glfw_init():
    width: int = 520
    height: int = 385
    window_name = "Dark and Darker Util"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    # Remove title bar so ImGui window can take over
    # Nevermind, keep windows title bar and disable ImGui's title bar
    # glfw.window_hint(glfw.DECORATED, glfw.FALSE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


if __name__ == "__main__":
    main()
