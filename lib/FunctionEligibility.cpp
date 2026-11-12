#include "minishield/FunctionEligibility.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/Support/Casting.h"

namespace minishield {
    EligibilityResult FunctionEligibility::check(const llvm::Function &F) {
        if (F.isDeclaration())
            return {false, "function has no body"};
        if (F.isPresplitCoroutine())
            return {false, "presplit coroutine is not supported"};
        if (F.hasPersonalityFn())
            return {false, "exception-handling personality is unsupported"};
        for (const llvm::BasicBlock &bb : F){
            for (const llvm::Instruction &I : bb) {
                if (const auto *intrinsic = llvm::dyn_cast<llvm::IntrinsicInst>(&I)) {
                    if (intrinsic->getCalledFunction()->getName().starts_with("llvm.coro.")) {
                        return {false, "coroutine intrinsic is unsupported"};
                    }
                }
            }

            if (bb.hasAddressTaken())
                return {false, "address-taken basic block is unsupported"};
            if (bb.isEHPad())
                return {false, "exception-handling pad is unsupported"};
            switch (bb.getTerminator()->getOpcode()){
                case llvm::Instruction::CondBr:
                case llvm::Instruction::UncondBr:
                case llvm::Instruction::Switch:
                case llvm::Instruction::Ret:
                case llvm::Instruction::Unreachable:
                    break;
                default:
                    return {false, std::string("unsupported terminator: ") + bb.getTerminator()->getOpcodeName()};
            }
        };
        return {true, ""};
    
    };
} // namespace minishield
