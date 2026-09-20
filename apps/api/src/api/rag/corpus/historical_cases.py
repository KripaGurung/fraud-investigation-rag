from api.rag.corpus.schema import CorpusDocument


HISTORICAL_FRAUD_CASES: tuple[CorpusDocument, ...] = (
    CorpusDocument(
        document_reference="CASE-001",
        document_type="historical_fraud_case",
        title="Large International Transfer from Previously Domestic Account",
        source="synthetic_historical_case_corpus",
        content=(
            "A retail banking customer with a history of small domestic "
            "payments initiated a high-value international transfer to a "
            "previously unseen beneficiary. The transaction originated from "
            "a device that had not appeared in the customer's recent activity. "
            "The transfer amount was substantially higher than the customer's "
            "normal transaction range. The case was escalated for investigation "
            "because the combination of transaction size, new beneficiary, "
            "international destination, and unfamiliar device represented a "
            "significant deviation from the customer's historical behavior."
        ),
    ),
    CorpusDocument(
        document_reference="CASE-002",
        document_type="historical_fraud_case",
        title="Rapid Sequence of Small Card Transactions",
        source="synthetic_historical_case_corpus",
        content=(
            "A retail banking customer experienced a rapid sequence of small "
            "card transactions across several merchants within a short period. "
            "The individual transaction amounts were consistent with the "
            "customer's usual spending range, but the frequency of transactions "
            "was substantially higher than normal. Several transactions occurred "
            "within minutes of one another. The activity was escalated for "
            "investigation because the unusual transaction velocity and merchant "
            "pattern differed from the customer's typical card usage."
        ),
    ),
    CorpusDocument(
        document_reference="CASE-003",
        document_type="historical_fraud_case",
        title="Account Activity Following Unusual Login Location",
        source="synthetic_historical_case_corpus",
        content=(
            "A retail banking customer normally accessed online banking from "
            "a consistent location and known device. A new login was recorded "
            "from an unfamiliar location using a device that had not previously "
            "been associated with the account. Shortly afterward, the account "
            "initiated multiple transfers to newly added beneficiaries. The "
            "activity was escalated for investigation because the change in "
            "login location, unfamiliar device, and newly added beneficiaries "
            "differed from the customer's established account activity."
        ),
    ),
)
