from random import shuffle


def team_shuffle(names, numbers):
    i = 0
    number = True
    while number:
        temp = list(zip(numbers, names))
        shuffle(temp)
        skill, name = zip(*temp)
        length = len(skill)
        length2 = len(name)

        middle_index = length // 2
        middle_index2 = length2 // 2

        first_half_skill = skill[:middle_index]
        second_half_skill = skill[middle_index2:]

        first_Team = name[:middle_index]
        second_Team = name[middle_index:]

        difference = sum(first_half_skill) - sum(second_half_skill)

        if sum(skill)/2 == sum(first_half_skill) or difference < 3 and difference > -4:
            number = False
            return first_Team + second_Team

        i += 1
        if i >= 100:
            break
