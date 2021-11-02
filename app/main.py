import psycopg2
from pip._vendor.distlib.compat import raw_input
from tabulate import tabulate
from lxml import etree

connection = psycopg2.connect(dbname='football_league', user='postgres', password='ligaliga', host='127.0.0.1')
cursor = connection.cursor()


def log_or_exit():
    while True:
        choice = raw_input('Do you want to login?[1-yes][0-no]: ')
        try:
            if 0 <= int(choice) <= 1:
                return int(choice)
            else:
                print('Error. Your choice was out of range. Try again.\n')
        except ValueError:
            print('Error. You did not type number. Try again.')


def log_in():
    print("Welcome to the football leagues database!")
    loggining = log_or_exit()
    if loggining == 0:
        cursor.close()
        connection.close()
        print("See you soon, goodbye!\n")
        exit()
    else:
        while True:
            login = str(raw_input('Type your login: '))
            query = "SELECT count(id) FROM users WHERE login = " + str("'" + login + "'")
            cursor.execute(query)
            result = cursor.fetchall()
            if 1 in result[0]:
                while True:
                    write = str(raw_input('Type your password: '))
                    query = "SELECT count(id) FROM users WHERE login = " + str(
                        "'" + login + "'") + " and password = crypt(" + str("'" + write + "'") + ", password)"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if 1 in result[0]:
                        query = "SELECT user_status FROM users WHERE login = " + str(
                            "'" + login + "'") + " and password = crypt(" + str("'" + write + "'") + ", password)"
                        cursor.execute(query)
                        user = cursor.fetchall()
                        return user[0][0]
                    else:
                        print('\nPassword is incorrect')
            print("Login that you typed does not exist. Try again.\n")


def main():
    print('\nFOOTBALL LEAGUES\n')
    user_type = log_in()
    while True:
        if user_type == "user":
            print("\nYou logged in as User!\n")
            user_main_menu()
        else:
            print("\nYou logged in as Admin!\n")
            admin_main_menu()
        choice = make_choice_in_menu()
        if choice == 0:
            user_type = log_in()
        elif choice == 1:
            show_table(cursor)
        elif choice == 2:
            show_query(cursor)
        elif choice == 3:
            execute_pro_query(cursor)
        elif choice == 4:
            export_table(cursor)
        elif choice == 5 and user_type == "admin":
            import_data()
        elif choice == 6 and user_type == "admin":
            update_data()


def user_main_menu():
    print("1 - Watch tables\n"
          "2 - Use prepared queries\n"
          "3 - Write your queries (for advanced users)\n"
          "4 - Export tables\n"
          "0 - Change user or exit\n")


def admin_main_menu():
    print("1 - Watch tables\n"
          "2 - Use prepared queries\n"
          "3 - Write your queries (for advanced users)\n"
          "4 - Export tables\n"
          "5 - Import your data\n"
          "6 - Update data\n"
          "0 - Change user or exit\n")


def make_choice_in_menu():
    choice = raw_input('Make a choice: ')
    try:
        if 0 <= int(choice) <= 6:
            return int(choice)
        else:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def show_tables_menu():
    print("\nTables:\n"
          "1 - league\n"
          "2 - team\n"
          "3 - season\n"
          "4 - team_position\n"
          "5 - player\n"
          "6 - match\n"
          "7 - personal_data\n"
          "8 - match_info\n"
          "9 - contract\n"
          "10 - transfer_cost\n"
          "11 - person_status\n"
          "0 - Back")


def choose_table():
    choice = raw_input('\nChoose table: ')
    try:
        if 0 <= int(choice) <= 11:
            return int(choice)
        else:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def show_table(cursor):
    show_tables_menu()
    move_back = False
    while not move_back:
        choice = choose_table()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            query_view(cursor, select='select * from public.league;', table_name='Leagues',
                       table_heads=['id', 'league_'])
        elif choice == 2:
            query_view(cursor, select='select * from public.team;', table_name='Teams',
                       table_heads=['id', 'league_id', 'team_'])
        elif choice == 3:
            query_view(cursor, select='select * from public.season;', table_name='Seasons',
                       table_heads=['id', 'season_'])
        elif choice == 4:
            query_view(cursor, select='select * from public.team_position', table_name='Teams Positions',
                       table_heads=['id', 'league_id', 'season_id', 'date', 'team_id', 'week', 'w_position', 'points'])
        elif choice == 5:
            query_view(cursor, select='select * from public.player;', table_name='Players',
                       table_heads=['id', 'personal_data_id', 'position', 'season_id'])
        elif choice == 6:
            query_view(cursor, select='select * from public.match;', table_name='Matches',
                       table_heads=['id', 'team1_id', 'team2_id', 'result', 'season_id', 'date'])
        elif choice == 7:
            query_view(cursor, select='select * from public.personal_data;', table_name='Personal data',
                       table_heads=['id', 'team_id', 'name', 'area', 'birthday', 'nationality', 'weight', 'height'])
        elif choice == 8:
            query_view(cursor, select='select * from public.match_info;', table_name='Match infos',
                       table_heads=['id', 'match_id', 'personal_data_id', 'minute', 'event'])
        elif choice == 9:
            query_view(cursor, select='select * from public.contract;', table_name='Contracts',
                       table_heads=['id', 'personal_data_id', 'fee', 'date_from', 'date_to'])
        elif choice == 10:
            query_view(cursor, select='select * from public.transfer_cost;', table_name='Transfer costs',
                       table_heads=['id', 'player_id', 'season_start', 'season_finish'])
        elif choice == 11:
            query_view(cursor, select='select * from public.person_status;', table_name='Persons statuses',
                       table_heads=['id', 'personal_data_id', 'match_id', 'match_status'])
        show_tables_menu()


def table_view(cursor, select, table_name, table_heads):
    cursor.execute(select)
    result = cursor.fetchall()
    print('\n' + table_name + '\n')
    print(tabulate(result, headers=table_heads, tablefmt='orgtbl'))


def show_queries_menu():
    print("\nQueries: \n"
          "1 - The list of the players who at the start of the season had value you enter "
          "and cost more than at the end.\n"
          "2 - End season results for the team with name you entered.\n"
          "3 - Events of the man with name you entered.\n"
          "4 - Squad of the team with name you entered.\n"
          "5 - Top 20 players with weight & height characteristics you choose.\n"
          "6 - Players with nationality you entered.\n"
          "7 - Number of players with assists & goals & substitutions characteristics you choose.\n"
          "0 - Back")


def characteristics():
    while True:
        print("\nTop 20: \n"
              "1 - The biggest weight.\n"
              "2 - The biggest height.\n"
              "3 - The smallest weight.\n"
              "4 - The smallest height.")
        tmp = raw_input('\nChoose : ')
        try:
            if 1 <= int(tmp) <= 4:
                return int(tmp)
            else:
                print('Error. Your choice was out of range. Try again.\n')
        except ValueError:
            print('Error. You did not type number. Try again.')


def event_type():
    while True:
        print("\nEvents: \n"
              "1 - Goals.\n"
              "2 - Assists.\n"
              "3 - Substitutions.")
        tmp = raw_input('\nChoose : ')
        try:
            if int(tmp) == 1:
                return "goal"
            if int(tmp) == 2:
                return "assist"
            if int(tmp) == 3:
                return "replaced"
            else:
                print('Error. Your choice was out of range. Try again.\n')
        except ValueError:
            print('Error. You did not type number. Try again.')


def seasons_or_leagues():
    while True:
        print("\nResults for: \n"
              "1 - Certain season.\n"
              "2 - Certain league.\n"
              "3 - All seasons and all leagues.\n"
              "4 - Certain season and certain league.")
        tmp = raw_input('\nChoose : ')
        try:
            if 1 <= int(tmp) <= 4:
                return int(tmp)
            else:
                print('Error. Your choice was out of range. Try again.\n')
        except ValueError:
            print('Error. You did not type number. Try again.')


def choose_query():
    choice = raw_input('\nChoose query: ')
    try:
        if 0 <= int(choice) <= 7:
            return int(choice)
        else:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def query_export(cursor, query):
    choice = raw_input('\nDo you want to export this query?[1-yes,0-no]')
    try:
        if int(choice) == 1:
            filename = raw_input('\nType filename: ')
            cursor.execute("COPY(" + query + ") TO 'D:\\Files\\Football_league\\console_app\\export_queries\\" + str(
                filename) + ".csv' CSV HEADER")
        elif int(choice) != 0:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def show_query(cursor):
    show_queries_menu()
    move_back = False
    while not move_back:
        choice = choose_query()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            tmp = raw_input('\nEnter cost: ')
            query = "SELECT season.season_, team.team_, personal_data.name, season_finish, season_start " \
                    "FROM transfer_cost JOIN personal_data on personal_data.id = player_id and " \
                    "season_finish > " + str("'" + tmp + "'") + " and season_start > " \
                                                                "season_finish JOIN player on player.id = player_id " \
                                                                "JOIN season on player.season_id = season.id JOIN " \
                                                                "team on team.id = personal_data.team_id"
            query_view(cursor, select=query, table_name='Cost: ' + str(tmp),
                       table_heads=['season', 'team', 'name', 'season_finish', 'season_start'])
        elif choice == 2:
            tmp = raw_input('\nEnter teams name: ')
            query = "SELECT season.season_, league.league_ as league, week, team.team_ as team, w_position, points " \
                    "FROM team_position JOIN team ON team_position.team_id = team.id and team.team_ = " + \
                    str("'" + tmp + "'") + " and week = 38 JOIN season ON season_id = season.id " \
                                           "JOIN league on league.id = team.league_id"
            query_view(cursor, select=query,
                       table_name='End season results for the team with name: ' + str(tmp),
                       table_heads=['season', 'league', 'week', 'team', 'w_position', 'points'])
        elif choice == 3:
            tmp = raw_input('\nEnter person name: ')
            query = "SELECT team.team_ as team, personal_data.name, match_id, minute, event FROM match_info JOIN " \
                    "personal_data on personal_data.name = " + str("'" + tmp + "'") \
                    + " and match_info.personal_data_id = personal_data.id JOIN team on team.id = personal_data.team_id"
            query_view(cursor, select=query, table_name='Man events with name: ' + str(tmp),
                       table_heads=['team', 'name', 'match_id', 'minute', 'event'])
        elif choice == 4:
            tmp = raw_input('\nEnter teams name: ')
            query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality FROM " \
                    "personal_data JOIN team ON team.id = personal_data.team_id and team_ = " + str("'" + tmp + "'") \
                    + " JOIN league on league.id = team.league_id"
            query_view(cursor, select=query, table_name='Squad of the team with name: ' + str(tmp),
                       table_heads=['league', 'team', 'name', 'birthday', 'nationality'])
        elif choice == 5:
            chr = characteristics()
            tmp = raw_input('\nEnter league name: ')
            if chr == 1:
                name = "Top 20 with the biggest weight in league: "
                query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality, weight, " \
                        "height FROM personal_data JOIN team ON team.id = personal_data.team_id JOIN " \
                        "league on league.league_ = " + str("'" + tmp + "'") \
                        + " and league.id = team.league_id order by weight DESC LIMIT 20"
            if chr == 2:
                name = "Top 20 with the biggest height in league: "
                query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality, weight, " \
                        "height FROM personal_data JOIN team ON team.id = personal_data.team_id JOIN " \
                        "league on league.league_ = " + str("'" + tmp + "'") \
                        + " and league.id = team.league_id order by height DESC LIMIT 20"
            if chr == 3:
                name = "Top 20 with the smallest weight in league: "
                query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality, weight, " \
                        "height FROM personal_data JOIN team ON team.id = personal_data.team_id JOIN " \
                        "league on league.league_ = " + str("'" + tmp + "'") \
                        + " and league.id = team.league_id order by weight LIMIT 20"
            if chr == 4:
                name = "Top 20 with the smallest height in league: "
                query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality, weight, " \
                        "height FROM personal_data JOIN team ON team.id = personal_data.team_id JOIN " \
                        "league on league.league_ = " + str("'" + tmp + "'") \
                        + " and league.id = team.league_id order by height LIMIT 20"
            query_view(cursor, select=query, table_name=name + str(tmp),
                       table_heads=['league', 'team', 'name', 'birthday', 'nationality', 'weight', 'height'])
        elif choice == 6:
            tmp = raw_input('\nEnter nationality: ')
            query = "SELECT league.league_ as league, team.team_ as team, name, birthday, nationality FROM " \
                    "personal_data JOIN team ON team.id = personal_data.team_id and nationality = " + \
                    str("'" + tmp + "'") + " JOIN league on league.id = team.league_id"
            query_view(cursor, select=query, table_name='List of players with nationality: ' + str(tmp),
                       table_heads=['league', 'team', 'name', 'birthday', 'nationality'])
        elif choice == 7:
            s_o_l = seasons_or_leagues()
            ev_type = event_type()
            if s_o_l == 1:
                tmp = raw_input('\nEnter season: ')
                limit = raw_input('\nEnter limit: ')
                name = "Top in certain season: "
                query = "select season.season_ as season, league.league_ as league, team.team_ as team, " \
                        "name, count(event) as goals from personal_data JOIN team on team.id = " \
                        "personal_data.team_id JOIN league on league.id = " \
                        "team.league_id JOIN match_info ON (personal_data.id = personal_data_id and event = " + \
                        str("'" + ev_type + "'") + ") JOIN match on match.id = " \
                                                   "match_info.match_id JOIN season on season.season_ = " + \
                        str("'" + tmp + "'") + " and season.id = match.season_id group by season.season_, " \
                                               "league.league_, team.team_, name order by count(event) DESC LIMIT " + \
                        str(limit)
                query_view(cursor, select=query, table_name=name,
                           table_heads=['season', 'league', 'team', 'name', 'count'])
            if s_o_l == 2:
                tmp = raw_input('\nEnter league: ')
                limit = raw_input('\nEnter limit: ')
                name = "Top in certain league: "
                query = "select league.league_ as league, team.team_ as team, " \
                        "name, count(event) as goals from personal_data JOIN team on team.id = " \
                        "personal_data.team_id JOIN league on league.league_ = " + \
                        str("'" + tmp + "'") + " and league.id = team.league_id JOIN match_info ON (" \
                                               "personal_data.id = personal_data_id and " \
                                               "event = " + str("'" + ev_type + "'") + ") JOIN match on match.id = " \
                                                                                       "match_info.match_id group by league.league_, team.team_, name order by count(event) DESC LIMIT " + str(
                    limit)
                query_view(cursor, select=query, table_name=name,
                           table_heads=['league', 'team', 'name', 'count'])
            if s_o_l == 3:
                limit = raw_input('\nEnter limit: ')
                name = "All time top: "
                query = "select league.league_ as league, team.team_ as team, " \
                        "name, count(event) as goals from personal_data JOIN team on team.id = " \
                        "personal_data.team_id JOIN league on league.id = " \
                        "team.league_id JOIN match_info ON (personal_data.id = personal_data_id and event = " + \
                        str("'" + ev_type + "'") + ") JOIN match on match.id = " \
                                                   "match_info.match_id group by league.league_, " \
                                                   "team.team_, name order by count(event) DESC LIMIT " + str(limit)
                query_view(cursor, select=query, table_name=name,
                           table_heads=['league', 'team', 'name', 'count'])
            if s_o_l == 4:
                tmps = raw_input('\nEnter season: ')
                tmpl = raw_input('\nEnter league: ')
                limit = raw_input('\nEnter limit: ')
                name = "Your top: "
                query = "select season.season_ as season, league.league_ as league, team.team_ as team, " \
                        "name, count(event) as cnt from personal_data JOIN team on team.id = " \
                        "personal_data.team_id JOIN league on league.league_ = " + \
                        str("'" + tmpl + "'") + " and league.id = team.league_id JOIN match_info ON (" \
                                                "personal_data.id = personal_data_id and event = " + \
                        str("'" + ev_type + "'") + ") JOIN match on match.id = match_info.match_id JOIN season on " \
                                                   "season.season_ = " + str(
                    "'" + tmps + "'") + " and season.id = match.season_id group by season.season_, league.league_, " \
                                        "team.team_, name order by count(event) DESC LIMIT " + str(limit)
                query_view(cursor, select=query, table_name=name,
                           table_heads=['season', 'league', 'team', 'name', 'count'])
        show_queries_menu()

        "1 - Certain season.\n"
        "2 - Certain league.\n"
        "3 - Certain season and certain league.\n"
        "4 - All seasons and all leagues."


def query_view(cursor, select, table_name, table_heads):
    try:
        cursor.execute(select)
        result = cursor.fetchall()
        print('\n' + table_name + '\n')
        print(tabulate(result, headers=table_heads, tablefmt='orgtbl'))
        print("\nThe number of rows in the result set : " + str(len(result)))
        query_export(cursor, select)
    except:
        connection.commit()
        print('Error. Input data is incorrect. Try again.')


def show_pro_queries_menu():
    print("\nPro queries: \n"
          "1 - Write query.\n"
          "0 - Back")


def choose_pro_query():
    choice = raw_input('\nChoose action: ')
    try:
        if 0 <= int(choice) <= 3:
            return int(choice)
        else:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def execute_pro_query(cursor):
    show_pro_queries_menu()
    move_back = False
    while not move_back:
        choice = choose_pro_query()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            try:
                tmp = raw_input('\nEnter your query: ')
                print("Your query: " + tmp)
                check_select = tmp.split(" ", 1)[0].lower()
                if check_select == "select":
                    query = str(tmp)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    print(tabulate(result))
                    print("The number of rows in the result set : " + str(len(result)))
                    query_export(cursor, query)
                else:
                    print("Error. You are only allowed to use SELECT here. Try again.")
            except:
                connection.commit()
                print('Error. Your query syntax is incorrect. Try again.')
        show_pro_queries_menu()


def export_table_data(cursor, query):
    choice = raw_input('\nDo you want to export this table?[1-yes,0-no]')
    try:
        if int(choice) == 1:
            filename = raw_input('\nType filename: ')
            cursor.execute("COPY(" + query + ") TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                filename) + ".csv' CSV HEADER")
        elif int(choice) != 0:
            print('Error. Your choice was out of range. Try again.\n')
    except ValueError:
        print('Error. You did not type number. Try again.')


def show_import_menu():
    print("\nImport: \n"
          "1 - Insert data.\n"
          "2 - Insert new user\n"
          "3 - Import xml file\n"
          "0 - Back")


def import_data():
    show_import_menu()
    move_back = False
    while not move_back:
        choice = choose_pro_query()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            try:
                tmp = raw_input('\nEnter your query: ')
                print("Your query: " + tmp)
                check_insert = tmp.split(" ", 1)[0].lower()
                if check_insert == "insert":
                    cursor.execute(tmp)
                    connection.commit()
                else:
                    print("Error. You are only allowed to use INSERT here. Try again.")
            except:
                connection.commit()
                print('Error. Your query syntax is incorrect. Try again.')
        elif choice == 2:
            try:
                name = raw_input('\nEnter user name: ')
                passw = raw_input('\nEnter user password: ')
                stat = raw_input('\nEnter user status: ')
                query = "INSERT INTO users (login,password,user_status) VALUES (" + str("'" + name + "', crypt(") + \
                        str("'" + passw + "',gen_salt('bf')), ") + str("'" + stat + "')")
                cursor.execute(query)
                connection.commit()
            except:
                connection.commit()
                print('Error. Your query syntax is incorrect or this login already exists. Try again.')
        elif choice == 3:
            root = etree.parse("D:\\Files\\Football_league\\console_app\\import.xml")
            for i in root.findall("personal_data"):
                p = [i.find(n).text for n in ("team_id", "name", "nationality", "birthday", "weight", "height")]
                query = ('INSERT INTO personal_data (team_id, name, nationality,birthday, weight,'
                         'height) VALUES (%s, %s, %s,%s,%s,%s)')
                vars = p[0], p[1], p[2], p[3], p[4], p[5]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in personal_data table.')
            for i in root.findall("match"):
                p = [i.find(n).text for n in ("team1_id", "team2_id", "result", "season_id", "date")]
                query = ('INSERT INTO match (team1_id, team2_id, result,season_id,date)'
                         ' VALUES (%s, %s, %s,%s,%s)')
                vars = p[0], p[1], p[2], p[3], p[4]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in match table.')
            for i in root.findall("contract"):
                p = [i.find(n).text for n in ("personal_data_id", "fee", "date_from", "date_to")]
                query = ('INSERT INTO contract (personal_data_id, fee, date_from, date_to)'
                         ' VALUES (%s, %s, %s,%s)')
                vars = p[0], p[1], p[2], p[3]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in contract table.')
            for i in root.findall("league"):
                p = i.find("league_").text
                query = ('INSERT INTO league (league_)'
                         ' VALUES (%s)')
                vars = p[0]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in league table.')
            for i in root.findall("match_info"):
                p = [i.find(n).text for n in ("match_id", "personal_data_id", "minute", "event")]
                query = ('INSERT INTO match_info (match_id, personal_data_id, minute, event)'
                         ' VALUES (%s, %s, %s,%s)')
                vars = p[0], p[1], p[2], p[3]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in match_info table.')
            for i in root.findall("person_status"):
                p = [i.find(n).text for n in ("personal_data_id", "match_id", "match_status")]
                query = ('INSERT INTO person_status (personal_data_id, match_id, match_status)'
                         ' VALUES (%s, %s, %s)')
                vars = p[0], p[1], p[2]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in person_status table.')
            for i in root.findall("player"):
                p = [i.find(n).text for n in ("personal_data_id", "position", "season_id")]
                query = ('INSERT INTO player (personal_data_id, position, season_id) VALUES (%s, %s, %s) where not exists (select personal_data_id,position,season_id from '
                         'player where personal_data_id = %s and position = %s and season_id = %s)')
                vars = p[0], p[1], p[2],p[0],p[1],p[2]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in player table.')
            for i in root.findall("season"):
                p = i.find("season_").text
                query = ('INSERT INTO season (season_)'
                         ' VALUES (%s)')
                vars = p[0]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in season table.')
            for i in root.findall("team"):
                p = [i.find(n).text for n in ("league_id", "team_")]
                query = ('INSERT INTO team (league_id,team_)'
                         ' VALUES (%s,%s)')
                vars = p[0], p[1]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in team table.')
            for i in root.findall("team_position"):
                p = [i.find(n).text for n in ("league_id", "season_id", "team_id", "week", "w_position", "points")]
                query = ('INSERT INTO team_position (league_id, season_id, team_id, week,w_position, points)'
                         ' VALUES (%s,%s,%s,%s,%s)')
                vars = p[0], p[1], p[2], p[3], p[4]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in team_position table.')
            for i in root.findall("transfer_cost"):
                p = [i.find(n).text for n in ("player_id", "season_start", "season_finish")]
                query = ('INSERT INTO transfer_cost (player_id, season_start, season_finish)'
                         ' VALUES (%s,%s,%s)')
                vars = p[0], p[1], p[2]
                try:
                    cursor.execute(query, vars)
                    connection.commit()
                except:
                    connection.commit()
                    print('Error. Data you are trying to import exists in transfer_cost table.')
        show_import_menu()


def show_update_menu():
    print("\nUpdate: \n"
          "1 - Update data.\n"
          "0 - Back")


def update_data():
    show_update_menu()
    move_back = False
    while not move_back:
        choice = choose_pro_query()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            try:
                tmp = raw_input('\nEnter your query: ')
                print("Your query: " + tmp)
                check_update = tmp.split(" ", 1)[0].lower()
                if check_update == "update":
                    cursor.execute(tmp)
                    connection.commit()
                else:
                    print("Error. You are only allowed to use UPDATE here. Try again.")
            except:
                connection.commit()
                print('Error. Your query syntax is incorrect. Try again.')
        show_update_menu()


def export_table(cursor):
    show_tables_menu()
    move_back = False
    while not move_back:
        choice = choose_table()
        if choice == 0:
            move_back = True
            break
        elif choice == 1:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM league) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 2:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM team) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 3:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM season) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 4:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM team_position) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 5:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM player) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 6:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM match) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 7:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM personal_data) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 8:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM match_info) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 9:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM contract) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 10:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM transfer_cost) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        elif choice == 11:
            filename = raw_input('\nType filename: ')
            cursor.execute(
                "COPY(SELECT * FROM person_status) TO 'D:\\Files\\Football_league\\console_app\\export_tables\\" + str(
                    filename) + ".csv' CSV HEADER")
        show_tables_menu()


if __name__ == '__main__':
    main()
