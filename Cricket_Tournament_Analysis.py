def enter_teams():
    while True:
        try:
            teams_count = int(input("Enter number of teams: "))
            if teams_count >= 2:
                break
            print("Minimum 2 teams should participate.")
        except ValueError:
            print("Enter valid integers.")

    teams = []
    while len(teams) < teams_count:
        name = input("Enter team name: ").strip()
        if name == "":
            print("Empty name entered!")
        elif name in teams:
            print("Duplicate teams are not allowed.")
        else:
            teams.append(name)
            print("Team added:", name)
    return teams


def create_stats(teams):
    stats = {}
    for team in teams:
        stats[team] = {
            "played": 0, "won": 0, "lost": 0, "tied": 0,
            "points": 0, "runs_scored": 0, "runs_conceded": 0,
            "balls_faced": 0, "balls_bowled": 0,
            "actual_balls_faced": 0, "actual_balls_bowled": 0
        }
    return stats


def validate_and_record_match(teams, stats, pair_count, number):
    print("\n---------------- MATCH", number, "----------------")
    team1 = input("Enter first team: ").strip()
    team2 = input("Enter second team: ").strip()

    if team1 not in teams or team2 not in teams:
        print("Teams not registered!")
        return False
    if team1 == team2:
        print("A team cannot play against itself.")
        return False

    if team1 < team2:
        pair = (team1, team2)
    else:
        pair = (team2, team1)

    if pair in pair_count and pair_count[pair] >= 2:
        print("These teams already played twice.")
        return False

    for team in [team1, team2]:
        while True:
            try:
                runs = int(input("Enter " + team + " runs: "))
                wickets = int(input("Enter " + team + " wickets (0-10): "))
                overs = int(input("Enter completed overs (0-20): "))
                balls = int(input("Enter remaining balls (0-5): "))

                if runs < 0:
                    print("Runs cannot be negative.")
                    continue
                if not 0 <= wickets <= 10:
                    print("Invalid wickets.")
                    continue
                if not 0 <= overs <= 20:
                    print("Invalid overs.")
                    continue
                if not 0 <= balls <= 5:
                    print("Invalid remaining balls.")
                    continue
                if overs == 20 and balls != 0:
                    print("No balls after 20 overs.")
                    continue

                total_balls = overs * 6 + balls
                if total_balls == 0:
                    print("At least one legal ball is required.")
                    continue

                if team == team1:
                    r1, w1, tb1 = runs, wickets, total_balls
                else:
                    r2, w2, tb2 = runs, wickets, total_balls
                break

            except ValueError:
                print("Invalid inputs. Enter integers.")

    actual_b1, actual_b2 = tb1, tb2

    if w1 == 10 and tb1 < 120:
        tb1 = 120
    if w2 == 10 and tb2 < 120:
        tb2 = 120

    stats[team1]["played"] += 1
    stats[team2]["played"] += 1

    stats[team1]["runs_scored"] += r1
    stats[team2]["runs_scored"] += r2
    stats[team1]["runs_conceded"] += r2
    stats[team2]["runs_conceded"] += r1

    stats[team1]["balls_faced"] += tb1
    stats[team2]["balls_faced"] += tb2
    stats[team1]["balls_bowled"] += tb2
    stats[team2]["balls_bowled"] += tb1

    stats[team1]["actual_balls_faced"] += actual_b1
    stats[team2]["actual_balls_faced"] += actual_b2
    stats[team1]["actual_balls_bowled"] += actual_b2
    stats[team2]["actual_balls_bowled"] += actual_b1

    if r1 > r2:
        stats[team1]["won"] += 1
        stats[team2]["lost"] += 1
        stats[team1]["points"] += 2
        print(team1, "wins!")
    elif r2 > r1:
        stats[team2]["won"] += 1
        stats[team1]["lost"] += 1
        stats[team2]["points"] += 2
        print(team2, "wins!")
    else:
        stats[team1]["tied"] += 1
        stats[team2]["tied"] += 1
        stats[team1]["points"] += 1
        stats[team2]["points"] += 1
        print("Match tied!")

    if pair in pair_count:
        pair_count[pair] += 1
    else:
        pair_count[pair] = 1

    print("Match recorded successfully.")
    print(team1, "score:", r1, "/", w1, "|", team2, "score:", r2, "/", w2)
    return True


def net_run_rate(stats, team):
    if stats[team]["balls_faced"] == 0 or stats[team]["balls_bowled"] == 0:
        return 0.00

    runrate = stats[team]["runs_scored"] * 6 / stats[team]["balls_faced"]
    conceded_rate = stats[team]["runs_conceded"] * 6 / stats[team]["balls_bowled"]
    return runrate - conceded_rate


def display_table(stats, teams):
    ranked = teams.copy()

    for i in range(len(ranked)):
        for j in range(len(ranked) - i - 1):
            team_a, team_b = ranked[j], ranked[j + 1]
            nrr_a, nrr_b = net_run_rate(stats, team_a), net_run_rate(stats, team_b)

            if (stats[team_a]["points"] < stats[team_b]["points"] or
                (stats[team_a]["points"] == stats[team_b]["points"] and nrr_a < nrr_b)):
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]

    print("\n" + "=" * 145)
    print("CRICKET TOURNAMENT - FINAL POINTS TABLE".center(145))
    print("=" * 145)
    print("Position".ljust(10), "Team".ljust(15), "Played".ljust(8), "Won".ljust(6),
          "Lost".ljust(6), "Tied".ljust(6), "Points".ljust(8), "RunsFor".ljust(9),
          "RunsAgainst".ljust(12), "OversFaced".ljust(20), "OversBowled".ljust(20), "NRR")
    print("-" * 145)

    position = 1
    for team in ranked:
        s = stats[team]
        nrr = net_run_rate(stats, team)

        faced = str(s["actual_balls_faced"] // 6) + " overs " + str(s["actual_balls_faced"] % 6) + " balls"
        bowled = str(s["actual_balls_bowled"] // 6) + " overs " + str(s["actual_balls_bowled"] % 6) + " balls"

        print(str(position).ljust(10), team.ljust(15), str(s["played"]).ljust(8),
              str(s["won"]).ljust(6), str(s["lost"]).ljust(6), str(s["tied"]).ljust(6),
              str(s["points"]).ljust(8), str(s["runs_scored"]).ljust(9),
              str(s["runs_conceded"]).ljust(12), faced.ljust(20), bowled.ljust(20),
              "{:.3f}".format(nrr))
        position += 1

    print("=" * 145)
    print("Tournament standings generated successfully.")


def main():
    print("\n" + "*" * 60)
    print("WELCOME TO CRICKET TOURNAMENT MANAGEMENT".center(60))
    print("*" * 60)

    teams = enter_teams()
    stats = create_stats(teams)
    pair_count = {}
    valid_teams = 0

    total_matches = len(teams) * (len(teams) - 1)
    print("\nRegistered teams:", ", ".join(teams))
    print("Total matches required:", total_matches)

    while valid_teams < total_matches:
        result = validate_and_record_match(teams, stats, pair_count, valid_teams + 1)
        if result:
            valid_teams += 1
            print("Matches completed:", valid_teams, "/", total_matches)
        else:
            print("Match rejected. Please enter the match again.")

    print("\n" + "*" * 60)
    print("TOURNAMENT COMPLETED".center(60))
    print("Total valid matches:", valid_teams)
    print("*" * 60)

    display_table(stats, teams)


if __name__ == "__main__":
    main()