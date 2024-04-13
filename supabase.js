importar { createClient } de '@supabase/supabase-js'

const supabaseUrl = processo . env .SUPABASE_URL
const supabaseKey = processo . env . DATABASE_KEY
const supabase = createClient ( supabaseUrl , supabaseKey )

export default supabase