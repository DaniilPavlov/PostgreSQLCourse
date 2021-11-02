import numpy
import psycopg2.extras as pgext
import random
import psycopg2

connection = psycopg2.connect(dbname='football_league', user='postgres', password='ligaliga', host='127.0.0.1')
cursor = connection.cursor()

countries = open("countries.txt", "r").readlines()
leagues = open("countries.txt", "r").readlines()
teams = open("teams.txt", "r").readlines()
first_names = open("first_name.txt", "r").readlines()
last_names = open("last_name.txt", "r").readlines()
tables = open("tables.txt", "r").readlines()
position_type = open("positions.txt", "r").readlines()

rint = random.randint


def clear_database():
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute("DELETE FROM {0} ".format(table))
            cursor.execute('ALTER SEQUENCE league_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE team_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE personal_data_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE contract_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE transfer_cost_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE player_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE match_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE season_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE match_info_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE team_position_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE person_status_id_seq RESTART')
    connection.commit()


def insert_in_table(table_name, values):
    if not values:
        return
    fields = ', '.join(values[0].keys())
    template = '(' + ', '.join('%({})s'.format(field) for field in values[0].keys()) + ')'
    pgsql = "INSERT INTO {} ({}) VALUES %s".format(table_name, fields)
    with connection.cursor() as cursor:
        pgext.execute_values(cursor, pgsql, values, template)
    connection.commit()


def generate_leagues(size):
    output = []
    i = 0
    while i != size:
        cur_league = random.choice(leagues).replace("\n", " ").replace(' ', '')
        query = "SELECT COUNT(league_) FROM league WHERE league_ LIKE " + "'" + cur_league + "'"
        cursor.execute(query)
        duplicate = cursor.fetchall()[0]
        if duplicate[0] > 0:
            print("Old {}".format(cur_league))
        else:
            output.append(
                {'league_': cur_league,
                 }
            )
            insert_in_table('league', output)
            output.clear()
            i = i + 1
    return 0


def generate_teams(size):
    query = "SELECT id FROM league"
    cursor.execute(query)
    id_league = cursor.fetchall()
    output = []
    arr_team = []
    for j in range(len(id_league)):
        query = "SELECT COUNT(team) FROM team WHERE league_id = " + str(id_league[j][0])
        cursor.execute(query)
        iftrue = cursor.fetchall()[0]
        arr_team.clear()
        i = 0
        if iftrue[0] == 0:
            while i != size:
                cur_team = random.choice(teams).replace("\n", " ").replace(' ', '')
                if cur_team not in arr_team:
                    output.append(
                        {
                            'team_': cur_team,
                            'league_id': id_league[j][0],
                        }
                    )
                    arr_team.append(cur_team)
                    i = i + 1
    return output


def generate_personal_datas(size):
    output = []
    query = "SELECT id FROM team"
    cursor.execute(query)
    id_team = cursor.fetchall()
    for j in range(len(id_team)):
        query = "SELECT COUNT(id) FROM personal_data WHERE team_id = " + str(id_team[j][0])
        cursor.execute(query)
        iftrue = cursor.fetchall()[0]
        if iftrue[0] == 0:
            for i in range(size):
                new_name = random.choice(first_names).replace("\n", " ").replace(' ', '') + " " \
                           + random.choice(last_names).replace("\n", " ").replace(' ', '')
                output.append(
                    {
                        'name': new_name,
                        'team_id': id_team[j][0],
                        'birthday': str(1984 + rint(0, 11)) + '-' + str(rint(1, 12)) + '-' + str(rint(1, 27)),
                        'nationality': random.choice(countries).replace("\n", " ").replace(' ', ''),
                        'weight': rint(50, 90),
                        'height': rint(161, 198),
                    }
                )
    return output


def generate_contracts(people_size, teams_size, leagues_size):
    output = []
    query = "SELECT id FROM personal_data"
    cursor.execute(query)
    id_personal = cursor.fetchall()
    for i in range(people_size * teams_size * leagues_size):
        query = "SELECT COUNT(id) FROM contract WHERE personal_data_id = " + str(id_personal[i][0])
        cursor.execute(query)
        iftrue = cursor.fetchall()[0]
        if iftrue[0] == 0:
            output.append(
                {
                    'personal_data_id': id_personal[i][0],
                    'fee': rint(10000, 450000),
                    'date_from': str(rint(2016, 2020)) + '-' + str(rint(1, 12)) + '-' + str(rint(1, 27)),
                    'date_to': str(rint(2021, 2026)) + '-' + str(rint(1, 12)) + '-' + str(rint(1, 27)),
                }
            )
    return output


def generate_seasons(seasons_size):
    output = []
    i = 0
    while i != seasons_size:
        cur_season = int(input("Type season: "))
        query = "SELECT COUNT(season_) FROM season WHERE season_ = " + str(cur_season)
        cursor.execute(query)
        duplicate = cursor.fetchall()[0]
        if duplicate[0] > 0:
            print("Old {}".format(cur_season))
        else:
            output.append(
                {'season_': cur_season,
                 }
            )
            insert_in_table('season', output)
            output.clear()
            i = i + 1
    return output


new_players = 0


def generate_players():
    global new_players
    query = "SELECT id FROM season"
    cursor.execute(query)
    id_season = cursor.fetchall()
    query = "SELECT id FROM personal_data"
    cursor.execute(query)
    id_personal = cursor.fetchall()
    output = []
    for j in range(len(id_season)):
        for i in range(len(id_personal)):
            query = "SELECT COUNT(position) FROM player WHERE personal_data_id = " + str(
                i + 1) + " and season_id = " + str(j + 1)
            cursor.execute(query)
            iftrue = cursor.fetchall()[0]
            if iftrue[0] == 0:
                new_players = new_players + 1
                output.append(
                    {
                        'personal_data_id': id_personal[i][0],
                        'position': random.choice(position_type),
                        'season_id': id_season[j][0],
                    }
                )
    return output


def generate_transfer_costs():
    output = []
    query = "SELECT id FROM player"
    cursor.execute(query)
    id_player = cursor.fetchall()
    for i in range(len(id_player)):
        query = "SELECT COUNT(id) FROM transfer_cost WHERE player_id = " + str(id_player[i][0])
        cursor.execute(query)
        iftrue = cursor.fetchall()[0]
        if iftrue[0] == 0:
            output.append(
                {
                    'player_id': id_player[i][0],
                    'season_start': int(round(rint(1000000, 150000000))),
                    'season_finish': int(round(rint(1000000, 150000000))),
                }
            )
    return output


match_results = []
match_teams = []


def rotate(l, n):
    return l[-n:] + l[:-n]


def generate_matches(teams_size):
    global old_matches
    output = []
    output2 = []
    cursor.execute("SELECT id FROM team")
    teams_id = cursor.fetchall()
    cur_id_count = 0
    id_count = 0
    query = "SELECT COUNT(id) FROM match"
    cursor.execute(query)
    old_matches = cursor.fetchall()[0]
    query = "SELECT COUNT(league_) FROM league"
    cursor.execute(query)
    cnt_league = cursor.fetchall()[0]
    query = "SELECT id FROM season"
    cursor.execute(query)
    id_season = cursor.fetchall()
    for m in range(len(id_season)):
        query = "SELECT season_ FROM season WHERE id = {}".format(id_season[m][0])
        cursor.execute(query)
        year = cursor.fetchall()[0]
        for j in range(cnt_league[0]):
            query = "SELECT COUNT(id) FROM match WHERE team1_id = " + str(
                teams_size * j + 1) + "and season_id = " + str(id_season[m][0])
            cursor.execute(query)
            iftrue = cursor.fetchall()[0]
            week = 0

            if iftrue[0] == 0:
                month = 8
                day = 1
                cur_id_count = cur_id_count + 1
                cur_id = teams_id[teams_size * j:(j + 1) * teams_size]
                points = [0] * 20
                for rs in range(teams_size):
                    points[rs] = 0
                while id_count != (cur_id_count) * (teams_size - 1) * int(round((teams_size / 2))):
                    step = 0
                    week += 1
                    flag = 0
                    day = day + 7
                    if day > 28:
                        day = 1
                        month = month + 1
                    while flag == 0:

                        id_count = id_count + 1
                        if id_count % int(round(teams_size / 2)) == 0:
                            flag = 1

                        first = rint(0, 4)
                        second = rint(0, 4)
                        if first > second:
                            points[step] = points[step] + 3
                        elif first < second:
                            points[teams_size - 1 - step] = points[teams_size - 1 - step] + 3
                        else:
                            points[step] = points[step] + 1
                            points[teams_size - 1 - step] = points[teams_size - 1 - step] + 1

                        cur_result = str(first) + '-' + str(second)
                        match_results.append(cur_result)
                        match_teams.append(str(cur_id[step]).replace("(", "").replace(')', '').replace(',', '') + "-" +
                                           str(cur_id[teams_size - 1 - step]).replace("(", "").replace(')', '').replace(
                                               ',',
                                               ''))
                        output.append(
                            {
                                'team1_id': cur_id[step],
                                'team2_id': cur_id[teams_size - 1 - step],
                                'result': cur_result,
                                'season_id': id_season[m][0],
                                'date': str(year[0]) + '-' + str(month) + '-' + str(day),
                            }
                        )
                        step = step + 1

                    o = 0
                    to_sort = numpy.zeros((20, 3))
                    for f in range(20):
                        to_sort[o][0] = o + 1
                        to_sort[o][1] = int(str(cur_id[f]).replace("(", "").replace(')', '').replace(',', ''))
                        to_sort[o][2] = points[f]
                        o += 1

                    for ff in range(19):
                        kek = ff
                        for aa in range(ff + 1, 20):
                            if (to_sort[aa][2] < to_sort[kek][2]):
                                kek = aa
                        to_sort[ff][1], to_sort[kek][1], to_sort[ff][2], to_sort[kek][2] = to_sort[kek][1], to_sort[ff][
                            1], to_sort[kek][2], to_sort[ff][2]

                    for qq in range(20):
                        output2.append(
                            {
                                'league_id': j + 1,
                                'season_id': id_season[m][0],
                                'team_id': to_sort[qq][1],
                                'week': week,
                                'w_position': 21 - to_sort[qq][0],
                                'points': to_sort[qq][2],
                            }
                        )
                    insert_in_table('team_position', output2)
                    output2.clear()

                    cur_id = rotate(cur_id[1:teams_size], 1)
                    cur_id.insert(0, teams_id[teams_size * j])
                month = 1
                day = 1
                cur_id_count = cur_id_count + 1
                while id_count != (cur_id_count) * (teams_size - 1) * int(round((teams_size / 2))):
                    week += 1
                    step = 0
                    flag = 0
                    day = day + 7
                    if day > 28:
                        day = 1
                        month = month + 1
                    while flag == 0:
                        id_count = id_count + 1
                        if id_count % int(round(teams_size / 2)) == 0:
                            flag = 1

                        first = rint(0, 4)
                        second = rint(0, 4)
                        if first > second:
                            points[teams_size - 1 - step] = points[teams_size - 1 - step] + 3
                        elif first < second:
                            points[step] = points[step] + 3
                        else:
                            points[step] = points[step] + 1
                            points[teams_size - 1 - step] = points[teams_size - 1 - step] + 1

                        cur_result = str(first) + '-' + str(second)
                        match_results.append(cur_result)
                        match_teams.append(
                            str(cur_id[teams_size - 1 - step]).replace("(", "").replace(')', '').replace(',', '') +
                            "-" + str(cur_id[step]).replace("(", "").replace(')', '').replace(',', ''))
                        output.append(
                            {
                                'team1_id': cur_id[teams_size - 1 - step],
                                'team2_id': cur_id[step],
                                'result': cur_result,
                                'season_id': id_season[m][0],
                                'date': str(year[0] + 1) + '-' + str(month) + '-' + str(day),
                            }
                        )
                        step = step + 1

                    o = 0
                    to_sort = numpy.zeros((20, 3))
                    for f in range(20):
                        to_sort[o][0] = o + 1
                        to_sort[o][1] = int(str(cur_id[f]).replace("(", "").replace(')', '').replace(',', ''))
                        to_sort[o][2] = points[f]
                        o += 1

                    for ff in range(19):
                        kek = ff
                        for aa in range(ff + 1, 20):
                            if (to_sort[aa][2] < to_sort[kek][2]):
                                kek = aa
                        to_sort[ff][1], to_sort[kek][1], to_sort[ff][2], to_sort[kek][2] = to_sort[kek][1], to_sort[ff][
                            1], to_sort[kek][2], to_sort[ff][2]

                    for qq in range(20):
                        output2.append(
                            {
                                'league_id': j + 1,
                                'season_id': id_season[m][0],
                                'team_id': to_sort[qq][1],
                                'week': week,
                                'w_position': 21 - to_sort[qq][0],
                                'points': to_sort[qq][2],
                            }
                        )
                    insert_in_table('team_position', output2)
                    output2.clear()

                    cur_id = rotate(cur_id[1:teams_size], 1)
                    cur_id.insert(0, teams_id[teams_size * j])
    return output


def generate_match_infos():
    output = []
    output3 = []
    i = old_matches[0]
    query = "SELECT id FROM match"
    cursor.execute(query)
    id_match = cursor.fetchall()
    res_count = 0
    while i != len(id_match):
        t1_g, t2_g = match_results[res_count].split("-")
        t1_, t2_ = match_teams[res_count].split("-")
        i = i + 1

        query = "SELECT id FROM personal_data WHERE team_id = {}".format(t1_)
        cursor.execute(query)
        team_persons = cursor.fetchall()
        main1 = 0
        mains = []
        subs = []
        sub1 = 0
        while main1 != 11:
            curr = random.choice(team_persons)
            if curr not in mains:
                mains.append(curr)
                main1 += 1
                output3.append(
                    {
                        'personal_data_id': curr,
                        'match_id': id_match[i - 1][0],
                        'match_status': 'main',
                    }
                )
                insert_in_table('person_status', output3)
                output3.clear()
        while sub1 != 6:
            curr = random.choice(team_persons)
            if curr not in mains and curr not in subs:
                subs.append(curr)
                sub1 += 1
                output3.append(
                    {
                        'personal_data_id': curr,
                        'match_id': id_match[i - 1][0],
                        'match_status': 'sub',
                    }
                )
                insert_in_table('person_status', output3)
                output3.clear()

        query = "SELECT id FROM personal_data WHERE team_id = {}".format(t2_)
        cursor.execute(query)
        team_persons = cursor.fetchall()
        main1 = 0
        mains = []
        subs = []
        sub1 = 0
        while main1 != 11:
            curr = random.choice(team_persons)
            if curr not in mains:
                mains.append(curr)
                main1 += 1
                output3.append(
                    {
                        'personal_data_id': curr,
                        'match_id': id_match[i - 1][0],
                        'match_status': 'main',
                    }
                )
                insert_in_table('person_status', output3)
                output3.clear()
        while sub1 != 6:
            curr = random.choice(team_persons)
            if curr not in mains and curr not in subs:
                subs.append(curr)
                sub1 += 1
                output3.append(
                    {
                        'personal_data_id': curr,
                        'match_id': id_match[i - 1][0],
                        'match_status': 'sub',
                    }
                )
                insert_in_table('person_status', output3)
                output3.clear()

        cursor.execute("SELECT id FROM personal_data WHERE team_id ={0}".format(t1_))
        players1 = cursor.fetchall()
        cursor.execute("SELECT id FROM personal_data WHERE team_id ={0}".format(t2_))
        players2 = cursor.fetchall()
        cursor.execute("SELECT personal_data_id FROM person_status WHERE match_status = " + "'" + "main" + "'")
        main_a = cursor.fetchall()

        main_p = []
        for nm in range(20):
            if players1[nm] in main_a:
                main_p.append(players1[nm])

        sub_times = rint(0, 3)
        z = 0
        subbed = []
        while z != sub_times:
            minute = str(rint(1, 96))
            flag = True
            while (flag):
                man = random.choice(main_p)
                if man not in subbed:
                    subbed.append(man)
                    output.append(
                        {
                            'match_id': id_match[i - 1][0],
                            'personal_data_id': man,
                            'minute': minute,
                            'event': 'replaced',
                        }
                    )
                    flag = False
                    z = z + 1

        for j in range(int(t1_g)):
            minute = str(rint(1, 96))
            man = random.choice(players1)
            output.append(
                {
                    'match_id': id_match[i - 1][0],
                    'personal_data_id': man,
                    'minute': minute,
                    'event': 'goal',
                }
            )
            flag = True
            while (flag):
                temp = random.choice(players1)
                if (man != temp):
                    flag = False
                    man = temp
            output.append(
                {
                    'match_id': id_match[i - 1][0],
                    'personal_data_id': man,
                    'minute': minute,
                    'event': 'assist',
                }
            )

        main_p = []
        for sm in range(20):
            if players2[sm] in main_a:
                main_p.append(players2[sm])

        sub_times = rint(0, 3)
        z = 0
        subbed = []
        while z != sub_times:
            minute = str(rint(1, 96))
            flag = True
            while (flag):
                man = random.choice(main_p)
                if man not in subbed:
                    subbed.append(man)
                    output.append(
                        {
                            'match_id': id_match[i - 1][0],
                            'personal_data_id': man,
                            'minute': minute,
                            'event': 'replaced',
                        }
                    )
                    flag = False
                    z = z + 1

        for j in range(int(t2_g)):
            minute = str(rint(1, 96))
            man = random.choice(players2)
            output.append(
                {
                    'match_id': id_match[i - 1][0],
                    'personal_data_id': man,
                    'minute': minute,
                    'event': 'goal',
                }
            )
            flag = True
            while (flag):
                temp = random.choice(players2)
                if (man != temp):
                    man = temp
                    flag = False
            output.append(
                {
                    'match_id': id_match[i - 1][0],
                    'personal_data_id': man,
                    'minute': minute,
                    'event': 'assist',
                }
            )
        res_count = res_count + 1
    return output


if __name__ == '__main__':
    clear = int(input("clear the table?:"))
    if clear:
        clear_database()

    seasons_size = 0
    leagues_size = 0

    if int(input("generate leagues?[1/0]")):
        leagues_size = int(input("How many?:"))
        league = generate_leagues(leagues_size)
        if int(input("generate teams?[1/0]")):
            teams_size = 20
            team = generate_teams(teams_size)
            insert_in_table('team', team)
            if int(input("generate personal datas?[1/0]")):
                people_size = int(input("How many (in each team)?:"))
                personal_data = generate_personal_datas(people_size)
                insert_in_table('personal_data', personal_data)
                if int(input("generate contracts?[1/0]")):
                    contracts = generate_contracts(people_size, teams_size, leagues_size)
                    insert_in_table('contract', contracts)

    if int(input("generate seasons?[1/0]")):
        seasons_size = int(input("How many?:"))
        seasons = generate_seasons(seasons_size)
        insert_in_table('season', seasons)
        if int(input("generate players?[1/0]")):
            players = generate_players()
            insert_in_table('player', players)
            if int(input("generate transfer costs?[1/0]")):
                transfer_cost = generate_transfer_costs()
                insert_in_table('transfer_cost', transfer_cost)

    if int(input("generate matches?[1/0]")):
        matches = generate_matches(20)
        insert_in_table('match', matches)
        if int(input("generate match infos?[1/0]")):
            match_infos = generate_match_infos()
            insert_in_table('match_info', match_infos)
