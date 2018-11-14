

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    
    def take_damage(self, amount):
        # passes log of action results back to engine.py (via return to ai.py) to handle
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    # TODO: Build a dictionary of alternative attack synonyms, randomly pick one for prints statement
    # print('You kick the ' + target.name + ' squarely in the nards, much to its dismay')
    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': '{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': '{0} attacks {1} but does no damage'.format(
                self.owner.name.capitalize(), target.name)})

        return results
    