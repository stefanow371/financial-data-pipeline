with
    source as (select * from {{ source("finance_raw", "transactions") }}),

    renamed as (
        select
            cast(transaction_id as string) as transaction_id,
            cast(transaction_date as date) as transaction_date,
            amount_original,
            upper(currency_original) as currency_original,
            cast(amount_target as numeric) as amount_target,
            upper(currency_target) as currency_target,
            trim(cost_center) as cost_center,
            vendor,
            lower(status) as status
        from source
    )

select *
from renamed
