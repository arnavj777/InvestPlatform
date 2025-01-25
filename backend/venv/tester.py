from simulation import simulation

sim = simulation('VOO')

sim.add_factor_to_dataset('RSI')
sim.add_factor_to_dataset('Volatility Ratio')
sim.add_entry_condition('RSI', '<=30')
sim.add_entry_condition('Volatility Ratio', ">=.2")
sim.add_exit_condition('RSI', '>=40')
sim.simulate()
sim.plot_sim()