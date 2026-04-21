from enum import StrEnum


class VulnerabilityType(StrEnum):
    Authorization_through_tx_origin = "Authorization_through_tx.origin"
    Delegatecall_to_Untrusted_Callee = "Delegatecall_to_Untrusted_Callee"
    Integer_Overflow_and_Underflow = "Integer_Overflow_and_Underflow"
    Presence_of_unused_variables = "Presence_of_unused_variables"
    Reentrancy = 'Reentrancy'
    Transaction_Order_Dependence = "Transaction_Order_Dependence"
    Unchecked_Call_Return_Value = "Unchecked_Call_Return_Value"
    Unprotected_Ether_Withdrawal = "Unprotected_Ether_Withdrawal"
    Assert_Violation = "Assert_Violation"
    Block_values_as_a_proxy_for_time = "Block_values_as_a_proxy_for_time"
    Code_With_No_Effects = "Code_With_No_Effects"
    DoS_with_Failed_Call = "DoS_with_Failed_Call"
    DoS_With_Block_Gas_Limit = "DoS_With_Block_Gas_Limit"
    Floating_Pragma = "Floating_Pragma"
    Function_Default_Visibility = "Function_Default_Visibility"
    Hash_Collisions_With_Multiple_Variable_Length_Arguments = "Hash_Collisions_With_Multiple_Variable_Length_Arguments"
    Incorrect_Inheritance_Order = "Incorrect_Inheritance_Order"
    Insufficient_Gas_Griefing = "Insufficient_Gas_Griefing"
    Lack_of_Proper_Signature_Verification = "Lack_of_Proper_Signature_Verification"
    Missing_Protection_against_Signature_Replay_Attacks = "Missing_Protection_against_Signature_Replay_Attacks"
    Outdated_Compiler_Version = "Outdated_Compiler_Version"
    Shadowing_State_Variables = "Shadowing_State_Variables"
    Signature_Malleability = "Signature_Malleability"
    State_Variable_Default_Visibility = "State_Variable_Default_Visibility"
    Uninitialized_Storage_Pointer = "Uninitialized_Storage_Pointer"
    Unprotected_SELFDESTRUCT_Instruction = "Unprotected_SELFDESTRUCT_Instruction"
    Weak_Sources_of_Randomness_from_Chain_Attributes = "Weak_Sources_of_Randomness_from_Chain_Attributes"
    Write_to_Arbitrary_Storage_Location = "Write_to_Arbitrary_Storage_Location"


class DetectMode(StrEnum):
    SOURCE_ONLY =  "SOURCE_ONLY",  # 仅源码检测
    CFG_ONLY = "CFG_ONLY",  # 仅控制流图检测
    SOURCE_AND_CFG = "SOURCE_AND_CFG",  # 源码 + 控制流图检测