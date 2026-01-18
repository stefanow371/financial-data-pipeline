with
    monthly_aggr as (
        select
            date_trunc(transaction_date, month) as reporting_month,
            cost_center,
            currency_target,
            round(sum(amount_target), 2) as total_burn,
            count(*) as transaction_count
        from {{ ref("stg_transactions") }}
        where status = 'paid'
        group by 1, 2, 3
    )

select
    *,
    lag(total_burn) over (
        partition by cost_center order by reporting_month
    ) as previous_month_burn,
    round(
        (
            total_burn
            - lag(total_burn) over (partition by cost_center order by reporting_month)
        ) / nullif(
            lag(total_burn) over (partition by cost_center order by reporting_month), 0
        )
        * 100,
        2
    ) as mom_pct_change
from monthly_aggr
