Čísla v ekonomickém přehledu kombinují potvrzená pravidla a modelové předpoklady. Model není statistickým měřením skutečné země, protože Larpidie je fikční projekt.

## Modelové ukazatele

- Populace: **{{fact.country.population|number}} obyvatel**.
- Průměrná hrubá mzda: **{{fact.economy.modelAverageGrossSalaryCzkMonthly|czk}} měsíčně**, modelová hodnota.
- Turistické návštěvy: **{{fact.economy.tourism.modelAnnualVisits|number}} ročně** v celé zemi, modelový předpoklad.
- Průměrná útrata návštěvy: **{{fact.economy.tourism.modelAverageSpendCzkPerVisit|czk}}**.
- Implikovaný turistický obrat: **{{calc.economy.tourismTurnoverCzk|czk}}**, nikoli příjem státního rozpočtu.

## Státní podniky a rámec služeb

Při modelovém rozdělitelném zisku státních podniků **{{fact.economy.stateEnterprises.modelDistributableProfitCzk|czk}}** a odvodech **{{fact.economy.stateEnterprises.transferToStatePercent|percent}}** vychází převod státu na **{{calc.economy.enterpriseStateTransferCzk|czk}}**. Do stabilizačního fondu jde **{{fact.economy.stateEnterprises.stabilizationFundPercentOfTransfer|percent}}** tohoto převodu, tedy **{{calc.economy.stabilizationFundCzk|czk}}**; z tohoto zdroje pak zbývá **{{calc.economy.enterpriseTransferAfterFundCzk|czk}}**.

Společný modelový rámec pro zdravotnictví a školství činí **{{fact.economy.healthEducationAnnualFrameworkCzk|czk}} ročně**. Jde o jednu společnou částku pro oba resorty.

## Ilustrační penzijní scénář

Modelový podíl obyvatel od {{fact.pensions.ageYears|number}} let je **{{fact.pensions.modelPopulation65PlusPercent|percent}}**, tedy **{{calc.economy.modelResidents65Plus|number}} lidí** z populace. Pokud by každý z nich byl larpidským občanem s nárokem na základní důchod, činil by součet nejvýše **{{calc.economy.maximumIllustrativeAnnualBasicPensionCzk|czk}} ročně**. Jde o maximální ilustrativní scénář, nikoli skutečný rozpočtový výdaj.

V omezeném bilančním scénáři se tento maximální penzijní odhad porovnává se společným rámcem zdravotnictví a školství a s běžnou částí modelovaného převodu podniků po rezervě. Potřeba dalších modelových příjmů v tomto srovnání činí **{{calc.economy.partialAdditionalFundingNeedCzk|czk}}**. Nejde o konečný schodek ani skutečně změřenou bilanci: odhad věkové skupiny neurčuje počet oprávněných občanů a výpočet nezahrnuje jiné příjmy a výdaje státu.

## Co nesčítat ani nezaměňovat

Turistické výdaje jsou obrat poskytovatelů, ne státní příjem ani automatické HDP. Tržby podniku nejsou jeho ziskem. Zisk podniku, daň z tohoto zisku a převod dividend do rozpočtu jsou tři odlišné položky. [Daňové sazby](#encyklopedie/ekonomika/dane) jsou uloženy centrálně.
