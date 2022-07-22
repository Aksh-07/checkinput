package py4j;



import java.util.ArrayList;



public class AppClass

{

    public String send_python_obj_to_java(ArrayList<Object> e)

    {

        return "success";

    }



    public String fill_data_for_speech_request(ArrayList<Object> a)

    {

        return "Success";

    }

    public String update_new_words_cloud(ArrayList<Object> b)

    {

        return "Success";

    }

    public String process_user_actions(ArrayList<Object> c)

    {

        return "Success";



    }

     public static void main(String[] args) {

        GatewayServer gatewayServer = new GatewayServer();

        GatewayServer.turnLoggingOff();

        gatewayServer.start();

        System.out.println("Gateway Server Started");

    }



}