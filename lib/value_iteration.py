#!/usr/local/bin/python2.7

# When it's a player's turn, she can
# flip the coin again and again until she
# gets a tail. Each time she flips, she will
# add one to her score if it's a head, but
# if it's a tail, she will lose not only
# her turn, but also all of her accumulated
# points for this turn.
#
# The question is, given the state of the game
# (her safe score, her score for this turn,
# and her opponent's score), what should the
# player do to maximize her probability of winning?

import random

GOAL = 5 # Win if you get to this point
THRESH = 0.001

# Init p values
p = {}
for safe_score in range(0, GOAL):
  for this_score in range(0, GOAL):
    for opp_score in range(0, GOAL):
      if safe_score + this_score >= GOAL:
        next
      elif opp_score >= GOAL:
        next
      else:
        p[(safe_score, this_score, opp_score)] = random.random()

# Iterate:
# v_s <- max_a sum_s' P^a_ss' (R^a_ss' + v_s')
worst_diff = 2 # the worst delta between p and new_p
best_action = {}
while worst_diff > THRESH:
  worst_diff = 0
  new_p = {}
  for state, prob in p.iteritems():
    safe_score = state[0]
    this_score = state[1]
    opp_score = state[2]
    if safe_score + this_score >= GOAL - 1:
      roll_again_success = 1 # We've won!
    else:
      roll_again_success = p[(safe_score, this_score + 1, opp_score)]
    roll_again_fail = 1 - p[(opp_score, 0, safe_score)]
    stop_rolling = 1 - p[(opp_score, 0, safe_score + this_score)]
    roll_again = 0.5 * (roll_again_success + roll_again_fail)
    if stop_rolling > roll_again:
      new_p[state] = stop_rolling
      best_action[state] = 'Stay'
    else:
      new_p[state] = roll_again
      best_action[state] = 'Roll'
    worst_diff = max(worst_diff, abs(new_p[state] - p[state]))
  p = new_p.copy()

# Sort by safe_score, then this_score, then opponent_score
def compare_states(x, y):
  return (x[0] - y[0]) * GOAL * GOAL + (x[1] - y[1]) * GOAL + (x[2] - y[2])

print("State (My Safe Score, My Risk Score, Opp. Score) / Best Action / Prob")
for state in sorted(new_p.keys(), cmp = compare_states):
  print("{0} / {1} / {2}".format(state, best_action[state], new_p[state]))
