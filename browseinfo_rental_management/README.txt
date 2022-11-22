1) version 15.0.0.1 (16/11/2021) :- "Improvements"
		- Added two fields i.e. weekly rental and daily rental on 'product.product' .
		- set rental value according to the selection for invoice [weekly,daily basis].
		- Improved code [removed raise Warning + replaced with raise UserError].

=> 15.0.0.2 : Add French, Spanish , Arabic and Dutch translation in module also improved an index.

15.0.0.3 (Dt. 13/01/2022) :- "Improvements" + "Fixes".
    - Improved start and end date fieldType date  to datetime.
    - Fixed rental flow for allowing hrs basis rental and also applied change on rental product lines.
    - Improved flow for replace rental products price_unit.
    - Removed Unwanted Code.
    - Added hourly rent field on rental product.
    - improved extend+ renewal functionality [added rental_initial_type + rental_initial field done proper
     calculations].

15.0.0.4 (Dt. 27/01/2022) :- "Improvements"
        - improved wizard validations for  rental terms and improved UI for extend wizard
15.0.0.5 (Dt. 18/02/2022)
        - fixed the rental order line product price value.
        - fixed cron issue[Expired Rental Email].
15.0.0.6 (Dt. 02/03/2022)
        - fixed replace product price issue
        - Improved code for rental history invoice amount
