# Generated from terraform.g4 by ANTLR 4.10.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .terraformParser import terraformParser
else:
    from terraformParser import terraformParser

# This class defines a complete listener for a parse tree produced by terraformParser.
class terraformListener(ParseTreeListener):

    # Enter a parse tree produced by terraformParser#file_.
    def enterFile_(self, ctx: terraformParser.File_Context):
        pass

    # Exit a parse tree produced by terraformParser#file_.
    def exitFile_(self, ctx: terraformParser.File_Context):
        pass

    # Enter a parse tree produced by terraformParser#terraform.
    def enterTerraform(self, ctx: terraformParser.TerraformContext):
        pass

    # Exit a parse tree produced by terraformParser#terraform.
    def exitTerraform(self, ctx: terraformParser.TerraformContext):
        pass

    # Enter a parse tree produced by terraformParser#resource.
    def enterResource(self, ctx: terraformParser.ResourceContext):
        pass

    # Exit a parse tree produced by terraformParser#resource.
    def exitResource(self, ctx: terraformParser.ResourceContext):
        pass

    # Enter a parse tree produced by terraformParser#data.
    def enterData(self, ctx: terraformParser.DataContext):
        pass

    # Exit a parse tree produced by terraformParser#data.
    def exitData(self, ctx: terraformParser.DataContext):
        pass

    # Enter a parse tree produced by terraformParser#provider.
    def enterProvider(self, ctx: terraformParser.ProviderContext):
        pass

    # Exit a parse tree produced by terraformParser#provider.
    def exitProvider(self, ctx: terraformParser.ProviderContext):
        pass

    # Enter a parse tree produced by terraformParser#output.
    def enterOutput(self, ctx: terraformParser.OutputContext):
        pass

    # Exit a parse tree produced by terraformParser#output.
    def exitOutput(self, ctx: terraformParser.OutputContext):
        pass

    # Enter a parse tree produced by terraformParser#local.
    def enterLocal(self, ctx: terraformParser.LocalContext):
        pass

    # Exit a parse tree produced by terraformParser#local.
    def exitLocal(self, ctx: terraformParser.LocalContext):
        pass

    # Enter a parse tree produced by terraformParser#module.
    def enterModule(self, ctx: terraformParser.ModuleContext):
        pass

    # Exit a parse tree produced by terraformParser#module.
    def exitModule(self, ctx: terraformParser.ModuleContext):
        pass

    # Enter a parse tree produced by terraformParser#variable.
    def enterVariable(self, ctx: terraformParser.VariableContext):
        pass

    # Exit a parse tree produced by terraformParser#variable.
    def exitVariable(self, ctx: terraformParser.VariableContext):
        pass

    # Enter a parse tree produced by terraformParser#block.
    def enterBlock(self, ctx: terraformParser.BlockContext):
        pass

    # Exit a parse tree produced by terraformParser#block.
    def exitBlock(self, ctx: terraformParser.BlockContext):
        pass

    # Enter a parse tree produced by terraformParser#blocktype.
    def enterBlocktype(self, ctx: terraformParser.BlocktypeContext):
        pass

    # Exit a parse tree produced by terraformParser#blocktype.
    def exitBlocktype(self, ctx: terraformParser.BlocktypeContext):
        pass

    # Enter a parse tree produced by terraformParser#resourcetype.
    def enterResourcetype(self, ctx: terraformParser.ResourcetypeContext):
        pass

    # Exit a parse tree produced by terraformParser#resourcetype.
    def exitResourcetype(self, ctx: terraformParser.ResourcetypeContext):
        pass

    # Enter a parse tree produced by terraformParser#name.
    def enterName(self, ctx: terraformParser.NameContext):
        pass

    # Exit a parse tree produced by terraformParser#name.
    def exitName(self, ctx: terraformParser.NameContext):
        pass

    # Enter a parse tree produced by terraformParser#label.
    def enterLabel(self, ctx: terraformParser.LabelContext):
        pass

    # Exit a parse tree produced by terraformParser#label.
    def exitLabel(self, ctx: terraformParser.LabelContext):
        pass

    # Enter a parse tree produced by terraformParser#blockbody.
    def enterBlockbody(self, ctx: terraformParser.BlockbodyContext):
        pass

    # Exit a parse tree produced by terraformParser#blockbody.
    def exitBlockbody(self, ctx: terraformParser.BlockbodyContext):
        pass

    # Enter a parse tree produced by terraformParser#argument.
    def enterArgument(self, ctx: terraformParser.ArgumentContext):
        pass

    # Exit a parse tree produced by terraformParser#argument.
    def exitArgument(self, ctx: terraformParser.ArgumentContext):
        pass

    # Enter a parse tree produced by terraformParser#identifier.
    def enterIdentifier(self, ctx: terraformParser.IdentifierContext):
        pass

    # Exit a parse tree produced by terraformParser#identifier.
    def exitIdentifier(self, ctx: terraformParser.IdentifierContext):
        pass

    # Enter a parse tree produced by terraformParser#identifierchain.
    def enterIdentifierchain(self, ctx: terraformParser.IdentifierchainContext):
        pass

    # Exit a parse tree produced by terraformParser#identifierchain.
    def exitIdentifierchain(self, ctx: terraformParser.IdentifierchainContext):
        pass

    # Enter a parse tree produced by terraformParser#inline_index.
    def enterInline_index(self, ctx: terraformParser.Inline_indexContext):
        pass

    # Exit a parse tree produced by terraformParser#inline_index.
    def exitInline_index(self, ctx: terraformParser.Inline_indexContext):
        pass

    # Enter a parse tree produced by terraformParser#expression.
    def enterExpression(self, ctx: terraformParser.ExpressionContext):
        pass

    # Exit a parse tree produced by terraformParser#expression.
    def exitExpression(self, ctx: terraformParser.ExpressionContext):
        pass

    # Enter a parse tree produced by terraformParser#forloop.
    def enterForloop(self, ctx: terraformParser.ForloopContext):
        pass

    # Exit a parse tree produced by terraformParser#forloop.
    def exitForloop(self, ctx: terraformParser.ForloopContext):
        pass

    # Enter a parse tree produced by terraformParser#section.
    def enterSection(self, ctx: terraformParser.SectionContext):
        pass

    # Exit a parse tree produced by terraformParser#section.
    def exitSection(self, ctx: terraformParser.SectionContext):
        pass

    # Enter a parse tree produced by terraformParser#val.
    def enterVal(self, ctx: terraformParser.ValContext):
        pass

    # Exit a parse tree produced by terraformParser#val.
    def exitVal(self, ctx: terraformParser.ValContext):
        pass

    # Enter a parse tree produced by terraformParser#functioncall.
    def enterFunctioncall(self, ctx: terraformParser.FunctioncallContext):
        pass

    # Exit a parse tree produced by terraformParser#functioncall.
    def exitFunctioncall(self, ctx: terraformParser.FunctioncallContext):
        pass

    # Enter a parse tree produced by terraformParser#functionname.
    def enterFunctionname(self, ctx: terraformParser.FunctionnameContext):
        pass

    # Exit a parse tree produced by terraformParser#functionname.
    def exitFunctionname(self, ctx: terraformParser.FunctionnameContext):
        pass

    # Enter a parse tree produced by terraformParser#functionarguments.
    def enterFunctionarguments(self, ctx: terraformParser.FunctionargumentsContext):
        pass

    # Exit a parse tree produced by terraformParser#functionarguments.
    def exitFunctionarguments(self, ctx: terraformParser.FunctionargumentsContext):
        pass

    # Enter a parse tree produced by terraformParser#index.
    def enterIndex(self, ctx: terraformParser.IndexContext):
        pass

    # Exit a parse tree produced by terraformParser#index.
    def exitIndex(self, ctx: terraformParser.IndexContext):
        pass

    # Enter a parse tree produced by terraformParser#filedecl.
    def enterFiledecl(self, ctx: terraformParser.FiledeclContext):
        pass

    # Exit a parse tree produced by terraformParser#filedecl.
    def exitFiledecl(self, ctx: terraformParser.FiledeclContext):
        pass

    # Enter a parse tree produced by terraformParser#list_.
    def enterList_(self, ctx: terraformParser.List_Context):
        pass

    # Exit a parse tree produced by terraformParser#list_.
    def exitList_(self, ctx: terraformParser.List_Context):
        pass

    # Enter a parse tree produced by terraformParser#map_.
    def enterMap_(self, ctx: terraformParser.Map_Context):
        pass

    # Exit a parse tree produced by terraformParser#map_.
    def exitMap_(self, ctx: terraformParser.Map_Context):
        pass

    # Enter a parse tree produced by terraformParser#string.
    def enterString(self, ctx: terraformParser.StringContext):
        pass

    # Exit a parse tree produced by terraformParser#string.
    def exitString(self, ctx: terraformParser.StringContext):
        pass

    # Enter a parse tree produced by terraformParser#signed_number.
    def enterSigned_number(self, ctx: terraformParser.Signed_numberContext):
        pass

    # Exit a parse tree produced by terraformParser#signed_number.
    def exitSigned_number(self, ctx: terraformParser.Signed_numberContext):
        pass

    # Enter a parse tree produced by terraformParser#operator_.
    def enterOperator_(self, ctx: terraformParser.Operator_Context):
        pass

    # Exit a parse tree produced by terraformParser#operator_.
    def exitOperator_(self, ctx: terraformParser.Operator_Context):
        pass

    # Enter a parse tree produced by terraformParser#number.
    def enterNumber(self, ctx: terraformParser.NumberContext):
        pass

    # Exit a parse tree produced by terraformParser#number.
    def exitNumber(self, ctx: terraformParser.NumberContext):
        pass


del terraformParser
