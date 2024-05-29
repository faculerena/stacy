;; Claim staking rewards per cycle
;; @desc: This function allows users to claim staking rewards for a given cycle
;; @param: x-token - The X token contract, y-token - The Y token contract, lp-token - The LP token contract, cycle - The cycle to claim rewards for
(define-public (claim-cycle-staking-rewards (x-token principal) (y-token principal) (lp-token principal) (x-token-trait <sip-010-trait>) (y-token-trait <sip-010-trait>) (lp-token-trait <sip-010-trait>) (cycle uint))
    (let
        (
            (current-cycle (contract-call? .stableswap get-current-cycle))
            (param-cycle-user-data (unwrap! (map-get? StakerDataPerCycleMap {x-token: x-token, y-token: y-token, lp-token: lp-token, user: tx-sender, cycle: cycle}) (err "err-no-cycle-data")))
            (param-cycle-reward-claimed (get reward-claimed param-cycle-user-data))
            (param-cycle-user-lp-staked (get lp-token-staked param-cycle-user-data))
            (param-cycle-total-lp-staked (unwrap! (map-get? DataPerCycleMap {x-token: x-token, y-token: y-token, lp-token: lp-token, cycle: cycle}) (err "err-no-cycle-data")))
            (param-cycle-fees (unwrap! (contract-call? .stableswap get-cycle-data x-token y-token lp-token cycle) (err "err-no-cycle-data")))
            (param-cycle-balance-x-fee (get cycle-fee-balance-x param-cycle-fees))
            (param-cycle-balance-y-fee (get cycle-fee-balance-y param-cycle-fees))
            (param-cycle-x-rewards (/ (* param-cycle-balance-x-fee param-cycle-user-lp-staked) param-cycle-total-lp-staked))
            (param-cycle-y-rewards (/ (* param-cycle-balance-y-fee param-cycle-user-lp-staked) param-cycle-total-lp-staked))
             (claimer tx-sender)
        )

        ;; Assert that param-cycle-x or param-cycle-y rewards are greater than 0
        (asserts! (or (> param-cycle-x-rewards u0) (> param-cycle-y-rewards u0)) (err "err-no-rewards-to-claim"))

        ;; Assert that param-cycle-reward-claimed is false
        (asserts! (not param-cycle-reward-claimed) (err "err-rewards-already-claimed"))

        ;; Assert that claiming from a previous cycle
        (asserts! (< cycle current-cycle) (err "err-cycle-too-high"))

        ;; Check if one of the param-cycle-x or param-cycle-y rewards is equal to 0
        (if (or (is-eq param-cycle-balance-x-fee u0) (is-eq param-cycle-balance-y-fee u0))
            ;; One of them is equal to 0, only transfer the other
            (if (is-eq param-cycle-balance-x-fee u0)
                ;; param-cycle-x-rewards is equal to 0, transfer param-cycle-y-rewards from contract to user
                 (unwrap! (as-contract (contract-call? y-token-trait transfer param-cycle-y-rewards tx-sender claimer none)) (err "err-y-token-transfer-failed"))
                ;; param-cycle-y-rewards is equal to 0, transfer param-cycle-x-rewards from contract to user
                 (unwrap! (as-contract (contract-call? x-token-trait transfer param-cycle-x-rewards tx-sender claimer none)) (err "err-x-token-transfer-failed"))
            )
            ;; Neither of them are equal to 0, transfer both
            (begin

                ;; Transfer param-cycle-x-rewards from contract to user
                (unwrap! (as-contract (contract-call? x-token-trait transfer param-cycle-x-rewards tx-sender claimer none)) (err "err-x-token-transfer-failed"))

                ;; Transfer param-cycle-y-rewards from contract to user
                (unwrap! (as-contract (contract-call? y-token-trait transfer param-cycle-y-rewards tx-sender claimer none)) (err "err-y-token-transfer-failed"))
            )
        )

        ;; Update StakerDataPerCycleMap with reward-claimed = true
        (map-set StakerDataPerCycleMap {x-token: x-token, y-token: y-token, lp-token: lp-token, user: claimer, cycle: cycle} (merge
            param-cycle-user-data
            {reward-claimed: true}
        ))

        (ok {x-token-reward: param-cycle-x-rewards, y-token-reward: param-cycle-y-rewards})
    ;;)
)
