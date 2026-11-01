Daňový systém Larpidie kombinuje daň ze zdanitelného zisku firem, daň z přidané hodnoty a progresivní pásma daně z příjmu fyzických osob. Všechny sazby v tomto článku jsou fikční pravidla, nikoli údaje o českém daňovém systému.

## Firmy a DPH

- Daň ze zdanitelného zisku firem: **{{fact.economy.corporateTaxPercent|percent}}**.
- Základní sazba DPH: **{{fact.economy.vat.standardPercent|percent}}**.
- Snížená sazba DPH: **{{fact.economy.vat.reducedPercent|percent}}**.

Snížená sazba se vztahuje na vybrané základní potřeby. Daň ze zisku se počítá ze zdanitelného zisku, ne z celého obratu. U státních podniků se navíc mohou odděleně rozdělovat dividendy a zisk ponechaný ve firmě; nejde o tutéž platbu jako firemní daň.

## Modelová daň z příjmů fyzických osob

Daň z příjmů využívá progresivní pásma s následujícími mezními sazbami:

| Roční zdanitelný příjem | Mezní sazba |
|---|---:|
| do {{fact.economy.personalIncomeTaxBrackets.0.upToAnnualCzk|number}} Kč | {{fact.economy.personalIncomeTaxBrackets.0.ratePercent|percent}} |
| {{fact.economy.personalIncomeTaxBrackets.0.upToAnnualCzk|number}} až {{fact.economy.personalIncomeTaxBrackets.1.upToAnnualCzk|number}} Kč | {{fact.economy.personalIncomeTaxBrackets.1.ratePercent|percent}} |
| {{fact.economy.personalIncomeTaxBrackets.1.upToAnnualCzk|number}} až {{fact.economy.personalIncomeTaxBrackets.2.upToAnnualCzk|number}} Kč | {{fact.economy.personalIncomeTaxBrackets.2.ratePercent|percent}} |
| nad {{fact.economy.personalIncomeTaxBrackets.2.upToAnnualCzk|number}} Kč | {{fact.economy.personalIncomeTaxBrackets.3.ratePercent|percent}} |

Jde o sazbu vztahovanou na příslušnou část základu v progresivním modelu, nikoli o tvrzení, že nejvyšší sazba platí na celý příjem každého poplatníka. Podrobnosti odpočtů, výjimek a technického výpočtu nejsou dokončené.

Číselné hodnoty jsou součástí veřejného ekonomického modelu.
