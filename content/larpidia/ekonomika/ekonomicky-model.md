Čísla v ekonomickém přehledu kombinují potvrzená pravidla a modelové předpoklady. Model není statistickým měřením skutečné země, protože Larpidie je fikční projekt.

## Modelové ukazatele

- Populace: **{{fact.country.population|number}} obyvatel**.
- Průměrná hrubá mzda: **{{fact.economy.modelAverageGrossSalaryCzkMonthly|czk}} měsíčně**, modelová hodnota.
- Turistické návštěvy: **{{fact.economy.tourism.modelAnnualVisits|number}} ročně** v celé zemi, modelový předpoklad.
- Průměrná útrata návštěvy: **{{fact.economy.tourism.modelAverageSpendCzkPerVisit|czk}}**.
- Implikovaný turistický obrat: **{{calc.economy.tourismTurnoverCzk|czk}}**, nikoli příjem státního rozpočtu.

## Státní podniky a rámec služeb

Při modelovém rozdělitelném zisku státních podniků **{{fact.economy.stateEnterprises.modelDistributableProfitCzk|czk}}** a odvodech **{{fact.economy.stateEnterprises.transferToStatePercent|percent}}** vychází převod státu na **{{calc.economy.enterpriseStateTransferCzk|czk}}**. Do stabilizačního fondu jde **{{fact.economy.stateEnterprises.stabilizationFundPercentOfTransfer|percent}}** tohoto převodu, tedy **{{calc.economy.stabilizationFundCzk|czk}}**; z tohoto zdroje pak zbývá **{{calc.economy.enterpriseTransferAfterFundCzk|czk}}**.

Společný modelový rámec pro zdravotnictví a školství činí **{{fact.economy.healthEducationAnnualFrameworkCzk|czk}} ročně**. Nejde o samostatný rozpočet pro každý z těchto resortů a nebylo prokázáno, že částka pokryje potvrzený rozsah služeb.

## Ilustrační penzijní scénář

Modelový podíl obyvatel od {{fact.pensions.ageYears|number}} let je **{{fact.pensions.modelPopulation65PlusPercent|percent}}**, tedy **{{calc.economy.modelResidents65Plus|number}} lidí** z populace. Pokud by každý z nich splňoval nárok na základní důchod, činil by součet **{{calc.economy.maximumIllustrativeAnnualBasicPensionCzk|czk}} ročně**. Jde o zjednodušený maximální ilustrační scénář; skutečný počet oprávněných příjemců není určen.

Po sečtení tohoto scénáře s rámcem zdravotnictví a školství a odečtení dostupného zisku podniků vychází **{{calc.economy.partialAdditionalFundingNeedCzk|czk}} částečné potřeby dalších prostředků**. **Není to konečný schodek rozpočtu.** Chybí mnoho příjmů, nákladů a financování jiných služeb. Při změně vstupních hodnot se tento výpočet přepočítá automaticky.

## Co nesčítat ani nezaměňovat

Turistické výdaje jsou obrat poskytovatelů, ne státní příjem ani automatické HDP. Tržby podniku nejsou jeho ziskem. Zisk podniku, daň z tohoto zisku a převod dividend do rozpočtu jsou tři odlišné položky. [Daňové sazby](#encyklopedie/ekonomika/dane) jsou uloženy centrálně.
