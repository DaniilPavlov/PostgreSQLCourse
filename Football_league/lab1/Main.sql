DROP TABLE IF EXISTS league,team,personal_data,transfer_cost,contract,player,match,match_info,person_status,team_position,users;
DROP TYPE IF EXISTS status, event_type;
DROP EXTENSION  pgcrypto;
CREATE EXTENSION pgcrypto;

CREATE TABLE IF NOT EXISTS public.users
(
    id          SERIAL      NOT NULL,
    login       TEXT        NOT NULL UNIQUE,
    password    TEXT        NOT NULL,
    user_status VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.league
(
    id      SERIAL      NOT NULL,
    league_ VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE league ADD UNIQUE (league_);

CREATE TABLE IF NOT EXISTS public.team
(
    id        SERIAL      NOT NULL,
    league_id int         NOT NULL,
    team_     VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT league_id_foreign
        FOREIGN KEY (league_id) REFERENCES public.league (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE team ADD UNIQUE (league_id, team_);

CREATE TABLE IF NOT EXISTS public.personal_data
(
    id          SERIAL       NOT NULL,
    team_id     int          NOT NULL,
    name        VARCHAR(100) NOT NULL,
    birthday    date         NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    weight      int          NOT NULL,
    height      int          NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT team_id_foreign
        FOREIGN KEY (team_id) REFERENCES public.team (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE personal_data ADD UNIQUE (team_id, name, nationality,birthday, weight, height);

CREATE TABLE IF NOT EXISTS public.contract
(
    id               SERIAL NOT NULL,
    personal_data_id int    NOT NULL,
    fee              int    NOT NULL,
    date_from        date   NOT NULL,
    date_to          date   NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT personal_id_foreign
        FOREIGN KEY (personal_data_id) REFERENCES public.personal_data (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE contract ADD UNIQUE (personal_data_id, fee, date_from, date_to);

CREATE TABLE IF NOT EXISTS public.season
(
    id      SERIAL NOT NULL,
    season_ int    NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE season ADD UNIQUE (season_);

CREATE TABLE IF NOT EXISTS public.event_types
(
    id   SERIAL      NOT NULL,
    type varchar(20) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.player
(
    id               SERIAL     NOT NULL,
    personal_data_id int        NOT NULL,
    position         VARCHAR(5) NOT NULL,
    season_id        int        NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT personal_id_foreign
        FOREIGN KEY (personal_data_id) REFERENCES public.personal_data (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT season_id_foreign
        FOREIGN KEY (season_id) REFERENCES public.season (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE player ADD UNIQUE (personal_data_id, season_id);

CREATE TABLE IF NOT EXISTS public.transfer_cost
(
    id            SERIAL NOT NULL,
    player_id     int    NULL,
    season_start  int    NOT NULL,
    season_finish int    NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT player_id_foreign
        FOREIGN KEY (player_id) REFERENCES public.player (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE transfer_cost ADD UNIQUE (player_id, season_start, season_finish);

CREATE TABLE IF NOT EXISTS public.match
(
    id        SERIAL      NOT NULL,
    team1_id  int         NOT NULL,
    team2_id  int         NOT NULL,
    result    VARCHAR(10) NOT NULL,
    season_id int         NOT NULL,
    date      date        NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT team1_id_foreign
        FOREIGN KEY (team1_id) REFERENCES public.team (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT team2_id_foreign
        FOREIGN KEY (team2_id) REFERENCES public.team (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    CONSTRAINT season_id_foreign
        FOREIGN KEY (season_id) REFERENCES public.season (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE match ADD UNIQUE (team1_id, team2_id, result,season_id,date);

CREATE TYPE status AS ENUM ('main', 'sub');

CREATE TABLE IF NOT EXISTS public.person_status
(
    id               SERIAL NOT NULL,
    personal_data_id int    NOT NULL,
    match_id         int    NOT NULL,
    match_status     status NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT personal_id_foreign
        FOREIGN KEY (personal_data_id) REFERENCES public.personal_data (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE person_status ADD UNIQUE (personal_data_id, match_id, match_status);

CREATE TYPE event_type AS ENUM ('goal', 'assist', 'replaced');

CREATE TABLE IF NOT EXISTS public.match_info
(
    id               SERIAL     NOT NULL,
    match_id         int        NULL,
    personal_data_id int        NOT NULL,
    minute           int        NOT NULL,
    event            event_type NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT match_id_foreign
        FOREIGN KEY (match_id) REFERENCES public.match (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,

    CONSTRAINT person_status_foreign
        FOREIGN KEY (personal_data_id) REFERENCES public.personal_data (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE match_info ADD UNIQUE (match_id, personal_data_id, minute, event);

CREATE TABLE IF NOT EXISTS public.team_position
(
    id         SERIAL NOT NULL,
    league_id  int    NOT NULL,
    season_id  int    NOT NULL,
    team_id    int    NOT NULL,
    week       int    NOT NULL,
    w_position int    NOT NULL,
    points     int    NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT league_id_foreign
        FOREIGN KEY (league_id) REFERENCES public.league (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,

    CONSTRAINT season_id_foreign
        FOREIGN KEY (season_id) REFERENCES public.season (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,

    CONSTRAINT team_id_foreign
        FOREIGN KEY (team_id) REFERENCES public.team (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

ALTER TABLE team_position ADD UNIQUE (league_id, season_id, team_id, week,points);

