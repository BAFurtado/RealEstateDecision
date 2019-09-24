### Ownership x Rental comparison for the case of Brazil

_By Bernardo Alves Furtado at Institute for Applied Economic and CNPq._

This is a simple numerical simulation that checks whether buying or renting is the best option, for a given set (of variable, uncertain) parameters. 

Publication currently under construction with details

## To run the model
1. `python comparisons.py` runs the comparison with the parameters set at params.py (you can change then manually) and outputs the money saved in present value if you choose do BUY a property
2. `python generalization.py` runs a comparison with the parameters listed at the bottom of the file. You can manually alter parameters. The output printed include the varied parameters and the present value of purchasing a property. 
3. If instead you run `python hyperspace.py` it outputs a figure with the chosen parameters variation and the present value output
4. Finally, running python randomizing.py gives you a list of outputs of purchasing present value. (you can change at the bottom of the file the number of times you want to randomically run the model.) And it plots the histogram of outputs.

### Notes for the Brazilian case:

Obs1. It is common practice that tenants pay for condominium and property taxes. So the burden falls for either owner or tenant

Obs2. There is no income tax deduction for mortgage interest paid    

Obs3. Taxes of 15% apply both in cash gains as well as increase in home values

Obs4. Years of payment plus age at signature cannot exceed 80 years. Thus, setting maximum age at 49 for contract day at 2019 and mortgage of maximum 30 years. Adjust accordingly.

Obs5. You can save a one-time run to a table by uncommenting the save steps in `comparisons.py`. SAVING option in comparisons.py needs to be set off to run `hyperspace` and `randomizing`

Obs6. Current implementation consider increases in RENT MARKET and HOUSE APPRECIATION are the same
