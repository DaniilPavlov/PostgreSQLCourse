import threading
import time
import matplotlib.pyplot as plotpy
import random
import psycopg2

connection = psycopg2.connect(dbname='football_league', user='postgres', password='ligaliga', host='127.0.0.1')
cursor = connection.cursor()
connection.autocommit = True

first_names = open("first_name.txt", "r").readlines()
last_names = open("last_name.txt", "r").readlines()
position_type = open("positions.txt", "r").readlines()
countries = open("countries.txt", "r").readlines()
match_results = open("results.txt", "r").readlines()
queries = open("queries.txt", "r").readlines()
rint = random.randint


def before_optimization(thread_cursor, query):
    if query == queries[0]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[0], {"team_id": rint(1, 140), "season_id": rint(1, 7)})
    elif query == queries[1]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[1], {"season_id": rint(1, 7), "result": random.choice(match_results)})
    elif query == queries[2]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[2], {"team_id": rint(1, 140)})
    elif query == queries[3]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[3], {"person": rint(1, 2800)})
    elif query == queries[4]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[4], {"team_id": rint(1, 140)})
    elif query == queries[5]:
        thread_cursor.execute("EXPLAIN ANALYZE " + queries[5], {"cost": rint(1000000, 150000000)})
    result = thread_cursor.fetchall()
    # print(result[-1][0])
    return float(result[-1][0].split(" ")[2])

def optima1(thread_cursor):
    thread_cursor.execute("explain analyze select personal_data.id, name, count(event) as cnt from personal_data JOIN "
                          "match_info ON (personal_data.id = personal_data_id and minute > 45 and event = 'goal') group by personal_data.id, name "
                          "order by count(event) DESC LIMIT 1")
    result = thread_cursor.fetchall()
    # print(result[-1][0])
    return float(result[-1][0].split(" ")[2])


def optima2(thread_cursor):
    thread_cursor.execute("EXPLAIN ANALYZE select id, name, top10.second_half_goals from personal_data JOIN (select max_sum.max_goals as second_half_goals, max_sum.person as name_id "
                          "from (select goals_sum.personal_data_id as person, sum(goals_sum.sh_goals) as max_goals "
                          "from (select personal_data_id, count(event) as sh_goals from match_info where minute > 45 and event = 'goal' "
                          "group by personal_data_id, minute, event) goals_sum group by goals_sum.personal_data_id) max_sum "
                          "order by max_sum.max_goals DESC LIMIT 10) as top10 ON id = top10.name_id order by top10.second_half_goals DESC")
    result = thread_cursor.fetchall()
    # print(result[-1][0])
    return float(result[-1][0].split(" ")[2])


query1 = queries[0]
query2 = queries[1]
query3 = queries[2]
query4 = queries[3]
query5 = queries[4]
query6 = queries[5]
optimized_queries = (query1, query2, query3, query4, query5, query6)


def drop_indexes():
    cursor.execute("DROP INDEX IF EXISTS team1_idx")
    cursor.execute("DROP INDEX IF EXISTS team2_idx")
    cursor.execute("DROP INDEX IF EXISTS season_idx")
    cursor.execute("DROP INDEX IF EXISTS result_idx")
    cursor.execute("DROP INDEX IF EXISTS person_team_idx")
    cursor.execute("DROP INDEX IF EXISTS person_idx")
    cursor.execute("DROP INDEX IF EXISTS team_pos_idx")
    cursor.execute("DROP INDEX IF EXISTS cost_finish_idx")
    cursor.execute("DROP INDEX IF EXISTS cost_start_idx")

    cursor.execute("DROP INDEX IF EXISTS pirs")
    cursor.execute("DROP INDEX IF EXISTS iven")
    cursor.execute("DROP INDEX IF EXISTS minu")


def create_indexes():
    cursor.execute("CREATE INDEX team1_idx ON match(team1_id)")
    cursor.execute("CREATE INDEX team2_idx ON match(team2_id)")
    cursor.execute("CREATE INDEX season_idx ON match(season_id)")
    cursor.execute("CREATE INDEX result_idx ON match(result)")
    cursor.execute("CREATE INDEX person_team_idx ON personal_data(team_id)")
    cursor.execute("CREATE INDEX person_idx ON match_info(personal_data_id)")
    cursor.execute("CREATE INDEX team_pos_idx ON team_position(team_id)")
    cursor.execute("CREATE INDEX cost_finish_idx ON transfer_cost(season_finish)")
    cursor.execute("CREATE INDEX cost_start_idx ON transfer_cost(season_finish)")

    cursor.execute("CREATE INDEX pirs ON personal_data(name)")
    cursor.execute("CREATE INDEX iven ON match_info(event)")
    cursor.execute("CREATE INDEX minu ON match_info(minute)")


def queries_optimization(thread_cursor):
    thread_cursor.execute(
        "PREPARE query1 (int, int) AS SELECT team.team_ as team, match.result, season.season_ as season, date "
        "FROM match JOIN team on team.id = $1 and (team2_id = team.id or team1_id = team.id ) "
        "JOIN season on season.id = $2 and match.season_id = season.id")
    thread_cursor.execute("PREPARE query2  (int, varchar) AS SELECT count(result) amount, season.season_ FROM match "
                          "JOIN season on season.id = $1 "
                          "WHERE match.result LIKE $2 and season_id = season.id group by season.season_")
    thread_cursor.execute("PREPARE query3  (int) AS SELECT name, birthday, nationality, team.team_ as team "
                          "FROM personal_data JOIN team ON team_id = $1 and team.id = team_id")
    thread_cursor.execute("PREPARE query4 (int) AS SELECT personal_data.name, match_id, minute, event "
                          "FROM match_info JOIN personal_data "
                          "on personal_data.id = $1 and match_info.personal_data_id = personal_data.id")
    thread_cursor.execute("PREPARE query5  (int) AS SELECT season.season_, week, team.team_ as team, w_position, points"
                          " FROM team_position JOIN team ON team_position.team_id = $1 and "
                          "team.id = team_position.team_id and week = 38 JOIN season ON season_id = season.id")
    thread_cursor.execute("PREPARE query6 (int) AS SELECT player_id, season_finish, season_start FROM transfer_cost "
                          "WHERE season_finish > $1 and season_start > season_finish")


def after_optimization(thread_cursor, query):
    if query == query1:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query1 (%s,%s)", [rint(1, 140), rint(1, 7)])
    elif query == query2:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query2 (%s,%s)",
                              [rint(1, 7), random.choice(match_results).replace("\n", " ").replace(' ', '')])
    elif query == query3:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query3 (%s)", [rint(1, 140)])
    if query == query4:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query4 (%s)", [rint(1, 2800)])
    elif query == query5:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query5 (%s)", [rint(1, 140)])
    elif query == query6:
        thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query6 (%s)", [rint(1000000, 150000000)])
    result = thread_cursor.fetchall()
    return float(result[-1][0].split(" ")[2]) + float(result[-2][0].split(" ")[2])


avg_respond_per_thread = []


def threads_stress(t_number, q_number):
    avg_respond_per_thread.clear()
    for i in range(t_number):
        current_thread = ThreadsWithQueries(i)
        current_thread.start()
    while threading.activeCount() > 1: time.sleep(1)
    plot_x = [g for g in range(100, q_number, 100)]
    plot_y = []
    for j in range(len(avg_respond_per_thread[0])):
        respond_time = 0
        for f in range(t_number): respond_time = avg_respond_per_thread[f][j] + respond_time
        plot_y.append(respond_time / t_number)
    plotpy.plot(plot_x, plot_y)
    plotpy.xlabel('Запросов в единицу времени')
    plotpy.ylabel('Затраты на один запрос, мс')
    if optimized:
        plotpy.title("После оптимизации. Потоков: {}".format(t_number))
    else:
        plotpy.title("До оптимизации. Потоков: {}".format(t_number))
    plotpy.show()


class ThreadsWithQueries(threading.Thread):
    def __init__(self, current_thread):
        self.current_thread = current_thread
        threading.Thread.__init__(self)
        self.conn = psycopg2.connect(dbname='football_league', user='postgres', password='ligaliga',
                                     host='127.0.0.1')
        self.cur = self.conn.cursor()
        if optimized: queries_optimization(self.cur)

    def run(self):
        if len(avg_respond_per_thread) <= self.current_thread:
            avg_respond_per_thread.append([])
        for i in range(100, query_number, 100):
            respond_time = []
            for j in range(0, i):
                if not optimized:
                    # random_query = random.choice(queries)
                    # respond_time.append(before_optimization(self.cur, random_query))
                    respond_time.append(optima2(self.cur))
                else:
                    # random_query = random.choice(optimized_queries)
                    # respond_time.append(after_optimization(self.cur, random_query))
                    respond_time.append(optima2(self.cur))
            avg_respond_per_thread[self.current_thread].append(sum(respond_time) / i)
        self.conn.commit()


if __name__ == "__main__":
    thread_number = 1
    query_number = 500
    drop_indexes()
    optimized = False
    threads_stress(thread_number, query_number)
    create_indexes()
    optimized = True
    threads_stress(thread_number, query_number)
