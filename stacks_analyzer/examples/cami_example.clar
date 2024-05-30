;; assert block height
(define-constant err-block-height (err u100))
(define-public (recipient principal) (
    (asserts! (> block-height 1000) err-block-height)
    (ft-transfer? stackaroo u50 (as-contract tx-sender) recipient)
    )
)
