from api.rag.corpus.schema import CorpusDocument


AML_FRAUD_POLICIES: tuple[CorpusDocument, ...] = (
    CorpusDocument(
        document_reference="POLICY-AML-001",
        document_type="aml_policy",
        title="Monitoring Significant Deviations from Customer Transaction Patterns",
        source="synthetic_aml_policy_corpus",
        content=(
            "Transaction monitoring should identify activity that represents "
            "a significant deviation from a customer's established transaction "
            "patterns. Relevant indicators may include unusually large transfer "
            "amounts, activity involving new beneficiaries, transactions involving "
            "locations not commonly associated with the customer, and access from "
            "previously unseen devices. A combination of multiple unusual indicators "
            "may warrant additional review to understand whether the activity is "
            "consistent with the customer's expected financial behavior."
        ),
    ),
    CorpusDocument(
        document_reference="POLICY-AML-002",
        document_type="aml_policy",
        title="Monitoring Unusual Transaction Velocity",
        source="synthetic_aml_policy_corpus",
        content=(
            "Transaction monitoring should identify unusually frequent activity "
            "within a short period when the frequency differs materially from a "
            "customer's established behavior. Relevant indicators may include "
            "multiple transactions occurring within minutes, activity across "
            "several merchants or beneficiaries, and sudden increases in the "
            "number of transactions. Unusual transaction velocity may warrant "
            "additional review even when individual transaction amounts are "
            "within the customer's normal range."
        ),
    ),
)
