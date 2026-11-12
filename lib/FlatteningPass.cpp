#include "minishield/FlatteningPass.h"
#include "minishield/FunctionEligibility.h"

#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
namespace minishield {

llvm::PreservedAnalyses FlatteningPass::run(
    llvm::Function &F,
    llvm::FunctionAnalysisManager &AM){
    if (F.isDeclaration())
        return llvm::PreservedAnalyses::all();
    
    const auto eligibility = FunctionEligibility::check(F);
    if (!eligibility.eligible) {
        llvm::errs() << "[MiniShield] rejected: " << F.getName() << ": " << eligibility.reason << "\n";
        return llvm::PreservedAnalyses::all();
    }

    llvm::errs() << "[MiniShield] eligible: " << F.getName() << "\n";

    return llvm::PreservedAnalyses::all();
}
} // namespace minishield
