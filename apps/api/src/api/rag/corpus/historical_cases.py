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
)
