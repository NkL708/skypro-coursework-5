from flask import Flask, render_template, request, redirect

from scripts.equipment import Equipment
from scripts.unit import BaseUnit, PlayerUnit, EnemyUnit
from scripts.classes import unit_classes
from scripts.base import Arena


app = Flask(__name__)

heroes = {
    'player': BaseUnit,
    'enemy': BaseUnit
}

arena = Arena()


@app.route('/')
def menu_page():
    return render_template('index.html')


@app.route('/fight/')
def start_fight():
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', 
                           heroes=heroes, 
                           battle_result='Бой начался!')


@app.route('/fight/hit')
def hit():
    if arena.game_is_running:
        arena.player_hit()
    return render_template('fight.html', 
                           heroes=heroes,
                           turn_result=arena.turn_result, 
                           battle_result=arena.battle_result)


@app.route('/fight/use-skill')
def use_skill():
    if arena.game_is_running:
        arena.player_use_skill()
    return render_template('fight.html', 
                           heroes=heroes,
                           turn_result=arena.turn_result, 
                           battle_result=arena.battle_result)


@app.route('/fight/pass-turn')
def pass_turn():
    arena.turn_result['player'] = ''
    if arena.game_is_running:
        arena.next_turn()
    return render_template('fight.html', 
                           heroes=heroes,
                           turn_result=arena.turn_result, 
                           battle_result=arena.battle_result)


@app.route('/fight/end-fight')
def end_fight():
    arena.battle_result = ''
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    equipment = Equipment()
    if request.method == 'GET':
        result = {
            'header': 'Выберете героя',
            'equipment': equipment,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        heroes['player'] = PlayerUnit(name=request.form['name'],
                                      unit_class=unit_classes[request.form['unit_class']])

        heroes['player'].equip_weapon(
            equipment.get_weapon(request.form['weapon']))
        heroes['player'].equip_armor(
            equipment.get_armor(request.form['armor']))
        return redirect('/choose-enemy/')


@app.route('/choose-enemy/', methods=['POST', 'GET'])
def choose_enemy():
    equipment = Equipment()
    result = {
        'header': 'Выберете врага',
        'equipment': equipment,
        'classes': unit_classes
    }
    if request.method == 'GET':
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        heroes['enemy'] = heroes['enemy']
        heroes['enemy'] = EnemyUnit(name=request.form['name'],
                                    unit_class=unit_classes[request.form['unit_class']])
        heroes['enemy'].equip_weapon(
            equipment.get_weapon(request.form['weapon']))
        heroes['enemy'].equip_armor(equipment.get_armor(request.form['armor']))
        return redirect('/fight/')


if __name__ == '__main__':
    app.run()
