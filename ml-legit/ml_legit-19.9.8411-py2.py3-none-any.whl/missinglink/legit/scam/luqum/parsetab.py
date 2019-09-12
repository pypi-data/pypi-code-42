
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftOR_OPleftAND_OPnonassocLPARENRPARENnonassocLBRACKETTORBRACKETnonassocPHRASEnonassocTERMAND_OP COLUMN LBRACKET LPAREN NOT OR_OP PHRASE QUOTATION_MARK RBRACKET RPAREN SEPARATOR SPLIT_FUNCTION TERM TOexpression : expression OR_OP expressionexpression : NOT expressionexpression : expression AND_OP expressionexpression : expression expressionexpression : LPAREN expression RPARENunary_expression : LBRACKET phrase_or_term TO phrase_or_term RBRACKETexpression : search_fieldsearch_field : SPLIT_FUNCTION COLUMN unary_expression COLUMN unary_expression COLUMN unary_expressionsearch_field : SPLIT_FUNCTION COLUMN unary_expression COLUMN unary_expressionsearch_field : SPLIT_FUNCTION COLUMN unary_expressionsearch_field : TERM COLUMN unary_expression\n        phrases_or_terms : phrases_or_terms phrase_or_term\n        phrases_or_terms : phrase_or_term\n        search_field : TERM COLUMN LPAREN phrases_or_terms RPARENunary_expression : PHRASEunary_expression : QUOTATION_MARK TERM QUOTATION_MARKunary_expression : TERMunary_expression : TOphrase_or_term : TERM\n                          | PHRASE'
    
_lr_action_items = {'NOT':([0,1,2,3,4,7,8,9,10,11,14,15,16,17,19,20,22,23,32,34,35,39,40,],[2,2,2,2,-7,2,2,2,2,2,-1,-3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'LPAREN':([0,1,2,3,4,7,8,9,10,11,13,14,15,16,17,19,20,22,23,32,34,35,39,40,],[3,3,3,3,-7,3,3,3,3,3,24,3,3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'SPLIT_FUNCTION':([0,1,2,3,4,7,8,9,10,11,14,15,16,17,19,20,22,23,32,34,35,39,40,],[5,5,5,5,-7,5,5,5,5,5,-1,-3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'TERM':([0,1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,40,],[6,6,6,6,-7,6,6,6,6,6,22,22,6,6,-5,-10,27,-18,-15,29,-17,-11,27,22,-19,-20,27,-13,-9,27,-16,-14,-12,22,-8,-6,]),'$end':([1,4,7,10,14,15,16,17,19,20,22,23,32,34,35,39,40,],[0,-7,-4,-2,-1,-3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'OR_OP':([1,4,7,10,11,14,15,16,17,19,20,22,23,32,34,35,39,40,],[8,-7,8,8,8,-1,-3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'AND_OP':([1,4,7,10,11,14,15,16,17,19,20,22,23,32,34,35,39,40,],[9,-7,9,9,9,9,-3,-5,-10,-18,-15,-17,-11,-9,-16,-14,-8,-6,]),'RPAREN':([4,7,10,11,14,15,16,17,19,20,22,23,27,28,30,31,32,34,35,36,39,40,],[-7,-4,-2,16,-1,-3,-5,-10,-18,-15,-17,-11,-19,-20,35,-13,-9,-16,-14,-12,-8,-6,]),'COLUMN':([5,6,17,19,20,22,32,34,40,],[12,13,25,-18,-15,-17,37,-16,-6,]),'LBRACKET':([12,13,25,37,],[18,18,18,18,]),'PHRASE':([12,13,18,24,25,27,28,30,31,33,36,37,],[20,20,28,28,20,-19,-20,28,-13,28,-12,20,]),'QUOTATION_MARK':([12,13,25,29,37,],[21,21,21,34,21,]),'TO':([12,13,25,26,27,28,37,],[19,19,19,33,-19,-20,19,]),'RBRACKET':([27,28,38,],[-19,-20,40,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,1,2,3,7,8,9,10,11,14,15,],[1,7,10,11,7,14,15,7,7,7,7,]),'search_field':([0,1,2,3,7,8,9,10,11,14,15,],[4,4,4,4,4,4,4,4,4,4,4,]),'unary_expression':([12,13,25,37,],[17,23,32,39,]),'phrase_or_term':([18,24,30,33,],[26,31,36,38,]),'phrases_or_terms':([24,],[30,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression OR_OP expression','expression',3,'p_expression_or','parser.py',145),
  ('expression -> NOT expression','expression',2,'p_expression_not','parser.py',150),
  ('expression -> expression AND_OP expression','expression',3,'p_expression_and','parser.py',155),
  ('expression -> expression expression','expression',2,'p_expression_implicit','parser.py',160),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_grouping','parser.py',165),
  ('unary_expression -> LBRACKET phrase_or_term TO phrase_or_term RBRACKET','unary_expression',5,'p_range','parser.py',170),
  ('expression -> search_field','expression',1,'p_expression_unary','parser.py',177),
  ('search_field -> SPLIT_FUNCTION COLUMN unary_expression COLUMN unary_expression COLUMN unary_expression','search_field',7,'p_split_function_3','parser.py',182),
  ('search_field -> SPLIT_FUNCTION COLUMN unary_expression COLUMN unary_expression','search_field',5,'p_split_function_2','parser.py',188),
  ('search_field -> SPLIT_FUNCTION COLUMN unary_expression','search_field',3,'p_split_function_1','parser.py',194),
  ('search_field -> TERM COLUMN unary_expression','search_field',3,'p_search_field','parser.py',200),
  ('phrases_or_terms -> phrases_or_terms phrase_or_term','phrases_or_terms',2,'p_phrases_or_terms','parser.py',210),
  ('phrases_or_terms -> phrase_or_term','phrases_or_terms',1,'p_phrases_or_terms','parser.py',211),
  ('search_field -> TERM COLUMN LPAREN phrases_or_terms RPAREN','search_field',5,'p_search_field_grouped','parser.py',220),
  ('unary_expression -> PHRASE','unary_expression',1,'p_quoting','parser.py',229),
  ('unary_expression -> QUOTATION_MARK TERM QUOTATION_MARK','unary_expression',3,'p_terms_quotation_mark','parser.py',234),
  ('unary_expression -> TERM','unary_expression',1,'p_terms','parser.py',239),
  ('unary_expression -> TO','unary_expression',1,'p_to_as_term','parser.py',245),
  ('phrase_or_term -> TERM','phrase_or_term',1,'p_phrase_or_term','parser.py',250),
  ('phrase_or_term -> PHRASE','phrase_or_term',1,'p_phrase_or_term','parser.py',251),
]
